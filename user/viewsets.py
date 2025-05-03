from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import get_user_model, login
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from .models import CustomUser
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


User = get_user_model()

class AuthViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    methods = ['post', 'get']
    serializer_class = RegisterSerializer

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=['get'])
    def csrf(self, request):
        return Response({'detail': 'CSRF cookie set'})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "Login successful!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, username=None):
        if username != request.user.username:
            return Response(
                {"detail": "You do not have permission to view this user."},
                status=status.HTTP_403_FORBIDDEN
            )


    def destroy(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
