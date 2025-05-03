from rest_framework import serializers
from django.contrib.auth import authenticate, login, get_user_model
from rest_framework import serializers
from django.shortcuts import get_object_or_404



User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"]
        )

        if not user:
            raise serializers.ValidationError({"detail": "User could not be created."})
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user = UserSerializer(read_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        
        if not user:
            raise serializers.ValidationError({"detail": "Invalid username or password."})
        
        user = get_object_or_404(User, username=user.username)

        data['user'] = user
        return data
    
    def to_representation(self, instance):
        """Custom output — serialize user properly."""
        return {
            "user": UserSerializer(self.validated_data["user"]).data
        }
    
class PasswordUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"detail": "Current password is incorrect."})
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError({"detail": "New password must be at least 8 characters long."})
        return value

