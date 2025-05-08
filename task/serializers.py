from rest_framework import serializers
from .models import Task
from user.models import CustomUser

class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False, allow_null=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'assignee',
            'status',
            'priority',
            'due_date',
            'created_on',
            'hive',
            'created_by'
        ]
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'assignee': {'required': False},
            'status': {'required': False},
            'priority': {'required': False},
            'due_date': {'required': False},
            'hive': {'required': False},
        }
