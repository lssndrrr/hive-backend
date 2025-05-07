from rest_framework import serializers
from .models import Hive, HiveMembership
from user.models import CustomUser

class HiveMemberUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class HiveMembershipSerializer(serializers.ModelSerializer):
    user = HiveMemberUserSerializer()

    class Meta:
        model = HiveMembership
        fields = ['user', 'role', 'joined_on']

class HiveSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Hive
        fields = ['id', 'name', 'description', 'members']

    def get_members(self, obj):
        memberships = obj.hive_membership.select_related('user').all()
        return HiveMembershipSerializer(memberships, many=True).data
