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
    
    @action(detail=True, methods=['delete'], url_path='member/(?P<user_id>[^/.]+)')
    def remove_member(self, request, pk=None, user_id=None):
        try:
            print(f"Removing user {user_id} from hive {pk}")
            hive = self.get_object()
            current_user_membership = HiveMembership.objects.get(hive=hive, user=request.user)
            member_to_remove = HiveMembership.objects.get(hive=hive, user__id=user_id)

            # Optionally: check if user is trying to remove themselves
            if member_to_remove.user == request.user:
                return Response({'detail': 'You cannot remove yourself.'}, status=status.HTTP_400_BAD_REQUEST)

            member_to_remove.delete()

            return Response({'message': 'Member removed successfully.'}, status=status.HTTP_200_OK)
        except HiveMembership.DoesNotExist:
            return Response({'detail': 'Member not found in hive.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            import traceback
            print("Unexpected error in remove_member:", traceback.format_exc())
            return Response({'detail': 'Failed to remove member.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['patch'], url_path='set_role/(?P<user_id>[^/.]+)')
    def set_role(self, request, pk=None, user_id=None):
        """
        Updates the role of a specific member within a hive.
        Expects {'role': 'NEW_ROLE'} in the request body.
        """
        new_role = request.data.get('role')

        if not new_role:
            return Response({'detail': 'New role is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the new role against the defined choices in your model
        valid_roles = [choice[0] for choice in HiveMembership.Role.choices] # Assuming Role is a TextChoices or similar enum
        if new_role not in valid_roles:
            return Response({'detail': f'Invalid role. Must be one of: {", ".join(valid_roles)}'}, status=status.HTTP_400_BAD_REQUEST)


        try:
            # Ensure the user setting the role is a member of the hive and has permission (e.g., Queen Bee)
            hive = self.get_queryset().get(pk=pk) # Ensure user is member of this hive
            current_user_membership = HiveMembership.objects.get(hive=hive, user=request.user)

            # Example Permission Check: Only Queen Bees can change roles
            if current_user_membership.role != HiveMembership.Role.QUEEN_BEE:
                return Response({'detail': 'Only the Queen Bee can change member roles.'}, status=status.HTTP_403_FORBIDDEN)


            # Get the membership object for the user whose role is being changed
            member_membership = HiveMembership.objects.get(hive=hive, user__id=user_id)

            # Prevent changing the Queen Bee's role or setting another Queen Bee (optional)
            if member_membership.role == HiveMembership.Role.QUEEN_BEE and new_role != HiveMembership.Role.QUEEN_BEE:
                return Response({'detail': 'Cannot change the Queen Bee\'s role directly.'}, status=status.HTTP_400_BAD_REQUEST)
            if member_membership.user == request.user and new_role != HiveMembership.Role.QUEEN_BEE:
                # Allow Queen Bee to step down, but maybe require a transfer?
                pass # Or add more complex logic for transferring QB role
            if new_role == HiveMembership.Role.QUEEN_BEE and member_membership.role != HiveMembership.Role.QUEEN_BEE:
                # Logic to ensure only one Queen Bee exists
                if HiveMembership.objects.filter(hive=hive, role=HiveMembership.Role.QUEEN_BEE).exclude(user=member_membership.user).exists():
                    return Response({'detail': 'A Queen Bee already exists in this hive.'}, status=status.HTTP_400_BAD_REQUEST)
                # If transferring Queen Bee role, you might demote the old one here


            member_membership.role = new_role
            member_membership.save()

            return Response({'message': f'Member role updated to {new_role} successfully.'}, status=status.HTTP_200_OK)

        except Hive.DoesNotExist:
            return Response({'detail': 'Hive not found or you are not a member.'}, status=status.HTTP_404_NOT_FOUND)
        except HiveMembership.DoesNotExist:
            return Response({'detail': 'Member not found in hive.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            import traceback
            print("Unexpected error in set_role:", traceback.format_exc())
            return Response({'detail': 'Failed to update member role.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
