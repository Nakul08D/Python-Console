from django.urls import include, path
from rest_framework import routers
from src.user.views import CodeExecutionViewSet
from src.user import views

router = routers.DefaultRouter(trailing_slash=False)
router.register("user", views.UserViewSet, basename="user")
router.register("code-execution", CodeExecutionViewSet, basename='code-execution')


urlpatterns = [
    path("", include(router.urls)),
]
