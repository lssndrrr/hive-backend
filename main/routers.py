from rest_framework import routers
from user.viewsets import AuthViewSet, UserViewSet
from task.viewsets import TaskViewSet
from hive.viewsets import HiveViewSet

# routers

router = routers.SimpleRouter()

router.register(r'auth', AuthViewSet, basename="auth")
router.register(r'user', UserViewSet, basename="user")
router.register(r'task', TaskViewSet, basename="task")
router.register(r'hive', HiveViewSet, basename='hive')


urlpatterns = router.urls