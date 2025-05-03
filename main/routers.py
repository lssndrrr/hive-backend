from rest_framework import routers
from user.viewsets import AuthViewSet, UserViewSet

# routers

router = routers.SimpleRouter()

router.register(r'auth', AuthViewSet, basename="auth")
router.register(r'user', UserViewSet, basename="user")


urlpatterns = router.urls