from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Hive, HiveMembership
from task.models import Task
from .serializers import HiveSerializer
from task.serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import status


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