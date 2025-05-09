from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Hive, HiveMembership
from task.models import Task
from .serializers import HiveSerializer
from task.serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from notifications.models import Invitation, Notification

User = get_user_model()

class HiveViewSet(viewsets.ModelViewSet):
    queryset = Hive.objects.all()
    serializer_class = HiveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Hive.objects.filter(hive_membership__user__username=self.request.user.username).distinct()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hive = serializer.save()

        HiveMembership.objects.create(
            user=request.user,
            hive=hive,
            role=HiveMembership.Role.QUEEN_BEE,
        )

        return Response({"message": "Hive created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        hives = self.get_queryset().prefetch_related(
            'hive_membership',
        )

        hive_ids = hives.values_list('id', flat=True)

        tasks = Task.objects.filter(hive_id__in=hive_ids).select_related(
            'hive', 'assignee', 'created_by'
        )

        hives_data = HiveSerializer(hives, many=True).data
        tasks_data = TaskSerializer(tasks, many=True).data
        print(hives_data, tasks_data)
        return Response({
            "message": "Hives fetched successfully.", 
            "data": {
                "hives": hives_data,
                "tasks": tasks_data
            }
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def invite_member(self, request):
        username = request.data.get('username')
        hive_id = request.data.get('hive')

        if not username or not hive_id:
            return Response({'detail': 'Username and hive ID are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_to_add = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            hive = Hive.objects.get(id=hive_id)
        except Hive.DoesNotExist:
            return Response({'detail': 'Hive not found.'}, status=status.HTTP_404_NOT_FOUND)

        if HiveMembership.objects.filter(user=user_to_add, hive=hive).exists():
            return Response({'detail': 'Member is already part of hive.'}, status=status.HTTP_409_CONFLICT)

        if Invitation.objects.filter(recipient=user_to_add, hive=hive).exists():
            return Response({'detail': 'Invite already sent.'}, status=status.HTTP_200_OK)

        message = f"You have been invited to join the hive '{hive.name}' by {request.user.username}."
        notification = Notification.objects.create(recipient=user_to_add, message=message, type=Notification.Type.INVITE)
        Invitation.objects.create(hive=hive, sender=request.user, recipient=user_to_add, notification=notification)

        return Response({'message': 'Invite sent successfully.'}, status=status.HTTP_201_CREATED)