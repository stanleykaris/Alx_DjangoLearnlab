from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import PostByTagListView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/update/', views.PostListView.as_view(), name='post_update'),
    path('tags/<str:tag_name>/', views.TaggedPostListView.as_view(), name='tagged_posts'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag')
]