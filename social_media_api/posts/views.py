from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from django.db.models import Q
from .models import Post, Comment, Like
from .serializers import CommentSerializer, PostSerializer
from rest_framework import filters, generics
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

# Create your views here.
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author == request.user
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class PostFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    content = CharFilter(lookup_expr='icontains')
    author = CharFilter(field_name='author__username', lookup_expr='iexact')
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'title']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
        return queryset
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['post']
    search_fields = ['content']
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)
        
    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.kwargs.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset
        
class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        user = self.request.user
        # Get posts from users that the current user follows
        # Include user's posts in the feed
        return Post.objects.filter(
            Q(author__in=user.following.all()) | Q(author=user)
        ).select_related('author').prefetch_related(
            'comments',
            'likes'
        ).order_by('-created_at')

class FeedViewWithFilters(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        user = self.request.user
        
        # Base queryset
        queryset = Post.objects.filter(
            Q(author__in=user.following.all()) | Q(author=user)
        ).select_related('author').prefetch_related(
            'comments',
            'likes'
        ).order_by('-created_at')
        
        # Apply filters
        time_filter = self.request.query_params.get('time', None)
        if time_filter:
            if time_filter == 'today':
                queryset = queryset.filter(created_at__date=timezone.now().date())
            elif time_filter == 'this_week':
                queryset = queryset.filter(created_at_gte=timezone.now() - timezone.timedelta(days=7))
            elif time_filter == 'this_month':
                queryset = queryset.filter(created_at_gte=timezone.now() - timezone.timedelta(days=30))
                
        # Filter by post type
        post_type = self.request.query_params.get('type', None)
        if post_type:
            queryset = queryset.filter(type=post_type)
            
        # Apply sorting
        sort_by = self.request.query_params.get('sort', '-created_at')
        valid_sort_fields = {
            'created_at': '-created_at',
            'likes': '-likes__count',
            'comments': '-comments__count'
        }
        
        sorted_field = valid_sort_fields.get(sort_by, '-created_at')
        return queryset.order_by(sorted_field)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
