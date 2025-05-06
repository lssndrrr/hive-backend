from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Hive, HiveMembership
from .serializers import HiveSerializer
from rest_framework.response import Response
from rest_framework import status


class HiveViewSet(viewsets.ModelViewSet):
    queryset = Hive.objects.all()
    serializer_class = HiveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Hive.objects.filter(hive_membership__user__username=self.request.user.username).distinct()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hive = serializer.save()

        HiveMembership.objects.create(
            user=request.user,
            hive=hive,
            role=HiveMembership.Role.QUEEN_BEE,
        )

        return Response({"message": "Hive created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)