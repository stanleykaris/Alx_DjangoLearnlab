from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import CustomUser, UserFollower

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'bio', 'profile_picture', 'followers', 'following']
        
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
            token = Token.objects.create(user=user)
        return user, token
    
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (['key'],)
    
class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'profile_picture', 'bio']
        
class FollowerListSerializer(serializers.ModelSerializer):
    from_user = UserFollowSerializer(read_only=True)
    to_user = UserFollowSerializer(read_only=True)
    followed_at = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = UserFollower
        fields = ['from_user', 'to_user', 'followed_at']    
    