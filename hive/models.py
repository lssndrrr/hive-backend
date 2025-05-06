from django.db import models
from user.models import CustomUser

# Create your models here.
class Hive(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class HiveMembership(models.Model):
    class Role(models.TextChoices):
        QUEEN_BEE = "QB", "Queen Bee",
        BUZZKEEPER = "BK", "Buzzkeeper",
        WORKER_BEE = "WORKER_BEE", "Worker Bee",
        
    role = models.CharField(max_length=50, choices=Role, default=Role.WORKER_BEE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_membership")
    hive = models.ForeignKey(Hive, on_delete=models.CASCADE, related_name="hive_membership")
    joined_on = models.DateTimeField(auto_now=False, auto_now_add=True)

