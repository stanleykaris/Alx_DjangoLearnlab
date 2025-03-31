from rest_framework import status, views, viewsets, filters
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction, models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from posts.models import Post
from .models import Notification, Like
from .serializer import NotificationSerializer
from django.utils import timezone

# Create your views here.
class LikeUnlikePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @transaction.atomic
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        
        # Check if user already liked post
        like, created = Like.objects.get_or_create(user=user, post=post)
        if created:
            if post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb='liked',
                    target=post,
                    action_object=like
                )
                
            return Response({
                'message': 'You liked this Post',
                'like_count': post.likes.count()
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            'message': 'You already liked this Post',
            'like_count': post.likes.count()
        }, status=status.HTTP_200_OK)
        
    @transaction.atomic
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        
        try:
            like = Like.objects.filter(actor=user, verb='liked', target=post)
            like.delete()
            
            # Remove the corresponding notification
            Notification.objects.filter(
                actor=user,
                verb='liked',
                target=post
            ).delete()
            
            return Response({
                'message': 'You unliked this Post',
                'like_count': post.likes.count()
            }, status=status.HTTP_200_OK)
            
        except Like.DoesNotExist:
            return Response({
                'message': 'You have not liked this Post',
                'like_count': post.likes.count()
            }, status=status.HTTP_404_NOT_FOUND)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'read_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related('actor', 'recipient').prefetch_related('target', 'action_object')
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'}, status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        unread_count = queryset.filter(read_at__isnull=True).count()
        
        status_filter = request.query_params.get('status', None)
        if status_filter:
            if status_filter == 'read':
                queryset = queryset.filter(read_at__isnull=False)
            elif status_filter == 'unread':
                queryset = queryset.filter(read_at__isnull=True)
                
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                response =self.get_paginated_response(serializer.data)
                response.data['unread_count'] = unread_count
                return response
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'results': serializer.data,
                'unread_count': unread_count
            })
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        self.get_queryset().filter(read_at__isnull=True).update(read_at=timezone.now())
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['delete'])
    def clear_all(self, request):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Notification Manager for creating notifications
class NotificationManager:
    @staticmethod
    def create_notification(recipient, actor, verb, target=None, action_object=None):
        if recipient != actor:
            return Notification.objects.create(
                recipient=recipient,
                actor=actor,
                verb=verb,
                target=target,
                action_object=action_object
            )
        return None
    
    @staticmethod
    def create_follow_notification(follower, followed_user):
        return NotificationManager.create_notification(
            recipient=followed_user,
            actor=follower,
            verb='started following you',
            target=followed_user
        )
        
    @staticmethod
    def create_like_notification(user, post):
        return NotificationManager.create_notification(
            recipient=post.author,
            actor=user,
            verb='liked your post',
            target=post
        )
        
    @staticmethod
    def create_comment_notification(comment):
        return NotificationManager.create_notification(
            recipient=comment.post.author,
            actor=comment.author,
            verb='commented on your post',
            target=comment.post,
            action_object=comment
        )
        
    def create_mention_notifications(self, comment):
        mentioned_users = comment.get_mentioned_users()
        if mentioned_users:
            for mentioned_user in mentioned_users:
                if mentioned_user not in [comment.author, comment.post.author]:
                    NotificationManager.create_notification(
                        recipient=mentioned_user,
                        actor=comment.author,
                        verb='mentioned you in a comment',
                        target=comment.post,
                        action_object=comment
                    )
    
@receiver(post_save, sender='accounts.UserFollower')
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        NotificationManager.create_follow_notification(instance.from_user, instance.to_user)
        
@receiver(post_save, sender='posts.Like')
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        NotificationManager.create_like_notification(instance.user, instance.post)
        
@receiver(post_save, sender='posts.Comment')
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        NotificationManager.create_comment_notification(instance)
        NotificationManager.create_mention_notifications(instance)               