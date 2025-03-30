from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView
from django.urls import include

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('feed/<int:user_id>/', FeedView.as_view(), name='user-feed'),
    path('posts/<int:pk>/like/',)
]