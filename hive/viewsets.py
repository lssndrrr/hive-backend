from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Hive, HiveMembership
from .serializers import HiveSerializer


class HiveViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HiveSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Hive.objects.filter(hive_membership__user__username=self.request.user.username).distinct()
