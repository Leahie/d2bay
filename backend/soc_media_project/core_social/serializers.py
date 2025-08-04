from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Profile, Trade, Comment, Like, FollowingRelationships

class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    followers_count = serializers.IntegerField(read_only=True)  
    following_count = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(source='full_name', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'birth_date', 'profile_picture', 'bio', 'location', 'interests', 'followers_count', 'following_count']

    def update(self, instance, validated_data):
        if "profile_picture" not in validated_data or not validated_data["profile_picture"]:
            validated_data["profile_picture"] = instance.profile_picture
        return super().update(instance, validated_data)
    
class ProfileListSerializer(ProfileSerializer):
    full_name = serializers.SerializerMethodField()
    followed_by_me = serializers.BooleanField(read_only=True)

    class Meta: 
        model = Profile 
        fields = ("id", "profile_picture", 'user', 'followed_by_me')
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_full_name(self, obj):
        return obj.full_name
    
class FollowingRelationshipsSerializer(serializers.ModelSerializer):
    profile_id = serializers.IntegerField(source = 'following.id', read_only = True)
    username = serializers.CharField(source = 'following.user.username')

    class Meta:
        model = FollowingRelationships
        fields = ("profile_id", "username")

class FollowerRelationshipsSerializers(serializers.ModelSerializer):
    profile_id = serializers.IntegerField(source = 'follower.id', read_only = True)
    username = serializers.CharField(source = 'follower.user.username')

    class Meta:
        model = FollowingRelationships 
        fields = ("profile_id", "username")

class ProfileDetailSerializer(ProfileSerializer):
    followers = FollowerRelationshipsSerializers(many = True, read_only = True)
    following = FollowingRelationshipsSerializer(many = True, read_only = True)

    class Meta:
        model = Profile
        fields = (
            "id", 
            "profile_picture", 
            "user_email", 
            "username", 
            "first_name", 
            "last_name", 
            "phone_number", 
            "birth_date", 
            "bio", 
            "followers", 
            "following", 
        )

class CommentSerializer(serializers.ModelSerializer):
    trade_id = serializers.IntegerField(source = "trade.id", read_only = True)
    author_username = serializers.CharField(source = "author.user.username", read_only = True)
    created_at = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Comment 
        fields = ("id", "author_username", "trade_id", "created_at")

class LikeSerializer(serializers.ModelSerializer):
    trade_id = serializers.IntegerField(source="trade.id", read_only=True)
    liked_by = serializers.CharField(source="profile.user.username", read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Like
        fields = ("id", "trade_id", "liked_by", "created_at")

class TradeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ("id", "image")

class TradeSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source = "author.user.username", read_only = True)
    author_full_name = serializers.CharField(source = "author.full_name", read_only = True)
    author_image = serializers.ImageField(source = "author.profile_image", read_only = True)
    image = serializers.ImageField(required = False, read_only = True)
    likes_count = serializers.IntegerField(read_only = True) 
    comments_count = serializers.IntegerField(read_only = True)

    class Meta: 
        model = Trade
        fields = (
            "id", 
            "author_username",
            "author_image", 
            "content", 
            "created_at", 
            "image",
            "likes_count", # counted when the set is queried in views
            "comments_count",
        )

class TradeListSerializer(TradeSerializer):
    liked_by_user = serializers.BooleanField(read_only=True)

    class Meta(TradeSerializer.Meta):
        fields = TradeSerializer.Meta.fields + ("liked_by_user",)


class TradeDetailSerializer(TradeSerializer):
    liked_by_user = serializers.BooleanField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta(TradeSerializer.Meta):
        fields = TradeSerializer.Meta.fields + (
            "liked_by_user",    
            "comments",
            "likes",
        )