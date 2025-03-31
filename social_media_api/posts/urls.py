from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, FeedViewWithFilters, LikePostView, UnlikePostView
from django.urls import include

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('feed/<int:user_id>/', FeedView.as_view(), name='user-feed'),
    path('feed/advanced/', FeedViewWithFilters.as_view(), name='feed-with-filters'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('api/', include('notifications.urls'))
]