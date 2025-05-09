from rest_framework import serializers
from .models import Notification, Invitation

class NotificationSerializer(serializers.ModelSerializer):
    invitation_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'type', 'created_at', 'is_read', 'invitation_id']

    def get_invitation_id(self, obj):
        if hasattr(obj, 'invitation'):
            return obj.invitation.id
        return None

class InvitationSerializer(serializers.ModelSerializer):
    hive_name = serializers.CharField(source='hive.name', read_only=True)
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)

    class Meta:
        model = Invitation
        fields = ['id', 'hive', 'hive_name', 'sender', 'sender_username', 'recipient', 'recipient_username', 'created_at', 'accepted']

