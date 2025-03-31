from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LikeUnlikePostView, NotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

url = [
    path()
]