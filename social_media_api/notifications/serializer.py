from rest_framework import serializers
from posts.models import Like
from .models import Notification
from django.utils import timezone

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        
class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    target = serializers.SerializerMethodField()
    action_object = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'actor', 'target', 'action_object', 'verb', 'created_at']
        
    def get_target(self, obj):
        if obj.target:
            return {
                'type': obj.action_object._meta.model_name,
                'id': obj.action_object.id,
                'str': str(obj.action_object)
            }
        return None
    
    def get_actor(self, obj):
        return {
            'type': obj.actor._meta.model_name,
            'id': obj.actor.id,
            'str': str(obj.actor)
        }
        
    def get_action_object(self, obj):
        if obj.action_object:
            return {
                'type': obj.action_object._meta.model_name,
                'id': obj.action_object.id,
                'str': str(obj.action_object)
            }
        return None
    
    def get_time_since(self, obj):
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 30:
            return obj.created_at.strftime("%b %d, %Y")
        elif diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"