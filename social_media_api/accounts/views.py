from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, TokenSerializer
from rest_framework import permissions
from .models import CustomUser, UserFollower

# Create your views here.
class RegisterUserView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class RetrieveTokenView(APIView):
    serializer_class = TokenSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, serializer.validated_data, status=status.HTTP_200_OK)
    
class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)
            
            # Preventing self-following
            if request.user == user_to_follow:
                return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
            
            _, created = UserFollower.objects.get_or_create(from_user=request.user, to_user=user_to_follow)
            if created:
                return Response(
                    {"message": f"You are now following {user_to_follow.username}"},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {"message": f"You are already following {user_to_follow.username}"},
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)
            follow_relationship = UserFollower.objects.get(from_user=request.user, to_user=user_to_unfollow)
            follow_relationship.delete()
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
        except UserFollower.DoesNotExist:
            return Response({'error': 'You are not following this user'}, status=status.HTTP_404_NOT_FOUND)
        
class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)
            request.user.following.remove(user_to_unfollow)
            return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class UserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class FollowersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        followers = request.user.followers.all()
        serializer = CustomUserSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserFollowStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id=None):
        user = request.user if user_id is None else CustomUser.objects.get(id=user_id)
        
        stats = {
            'username': user.username,
            'followers_count': user.followers.count(),
            'following_count': user.following.count(),
            'is_following': False
        }
        
        if request.user != user:
            stats['is_following'] = UserFollower.objects.filter(from_user=request.user, to_user=user).exists()
        return Response(stats, status=status.HTTP_200_OK)