from rest_framework import serializers
from .models import Hive, HiveMembership
from user.serializers import UserSerializer


class HiveMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = HiveMembership
        fields = ['user', 'role', 'joined_on']


class HiveSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Hive
        fields = ['id', 'name', 'description', 'members']

    def get_members(self, obj):
        memberships = HiveMembership.objects.filter(hive=obj).select_related('user')
        return HiveMemberSerializer(memberships, many=True).data
