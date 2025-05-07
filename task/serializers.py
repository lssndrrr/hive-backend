from rest_framework import serializers
from .models import Task
from rest_framework import serializers
from .models import Task
from user.models import CustomUser

class TaskUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assignee = TaskUserSerializer(allow_null=True)
    created_by = TaskUserSerializer()
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
