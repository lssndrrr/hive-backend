from rest_framework import serializers
from django.contrib.auth import authenticate, login
from rest_framework import serializers
from django.contrib.auth import get_user_model
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
