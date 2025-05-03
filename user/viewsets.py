from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator

from .models import CustomUser
from .serializers import LoginSerializer, RegisterSerializer

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
        print("here", serializer.is_valid())
        if serializer.is_valid():
            return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
        print("errors:", serializer.errors) 
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)