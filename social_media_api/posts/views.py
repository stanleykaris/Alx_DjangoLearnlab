from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from .models import Post, Comment, Like
from .serializers import CommentSerializer, PostSerializer
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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
        
class FeedView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
