from rest_framework import routers
from user.viewsets import AuthViewSet

# routers

router = routers.SimpleRouter()

router.register(r'auth', AuthViewSet, basename="auth")


urlpatterns = router.urls