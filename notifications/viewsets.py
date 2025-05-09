from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Invitation, Notification
from hive.models import HiveMembership
from .serializers import InvitationSerializer, NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')
    
class InvitationViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invitation.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['patch'])
    def accept(self, request, pk=None):
        invitation = self.get_object()
        if invitation.accepted is not None:
            return Response({'detail': 'Invitation already responded to.'}, status=status.HTTP_400_BAD_REQUEST)

        HiveMembership.objects.create(
            user=request.user,
            hive=invitation.hive,
            role=HiveMembership.Role.WORKER_BEE
        )
        invitation.accepted = True
        invitation.save()
        return Response({'detail': 'Invitation accepted.'})

    @action(detail=True, methods=['patch'])
    def decline(self, request, pk=None):
        invitation = self.get_object()
        if invitation.accepted is not None:
            return Response({'detail': 'Invitation already responded to.'}, status=status.HTTP_400_BAD_REQUEST)

        invitation.accepted = False
        invitation.save()
        return Response({'detail': 'Invitation declined.'})
