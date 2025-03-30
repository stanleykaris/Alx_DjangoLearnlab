from django.urls import path
from .views import RegisterUserView, LoginView, FollowUserView, UnfollowUserView, UserProfileView, FollowersListView, UserFollowStatsView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('followers/<int:user_id>/', FollowersListView.as_view(), name='followers-list'),
    path('followers/', FollowersListView.as_view(), name='followers-list'),
    path('follow-stats/', UserFollowStatsView.as_view(), name='follow-stats'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]