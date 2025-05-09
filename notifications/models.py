from django.db import models
from django.contrib.auth import get_user_model
from hive.models import Hive

User = get_user_model()

class Notification(models.Model):
    class Type(models.TextChoices):
        GENERAL = "GEN", "General Notification",
        INVITE = "INV", "Hive Invitation",
        REMINDER = "REM", "Task Reminder",
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    type = models.CharField(max_length=50, choices=Type)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"To {self.recipient}: {self.message[:30]}"

    
class Invitation(models.Model):
    hive = models.ForeignKey(Hive, on_delete=models.CASCADE, related_name='invitations')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(null=True)
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('hive', 'recipient')
