from django.db.models import Count, Q, OuterRef, Exists, Subquery
from django.shortcuts import render

#drf spectacular 
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

# rest framework
from rest_framework import mixins, status, viewsets
from rest_framework.generics import (
    get_object_or_404,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.response import Response


# permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

# models
from core_social.models import Profile, FollowingRelationships, Trade, Like, Comment
# serializers 
from core_social.serializers import (
    ProfileSerializer, 
    ProfileListSerializer, 
    ProfileDetailSerializer,
    FollowerRelationshipsSerializers, 
    FollowingRelationshipsSerializer, 
    TradeSerializer,
    TradeDetailSerializer,
    TradeImageSerializer,
    TradeListSerializer,
    CommentSerializer, 
    LikeSerializer,
)

# from core_social.permissions import IsAuthorOr  should I add or should I just use general permissions

# Create your views here.
class CurrentUserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Profile.objects.filter(user = self.request.user)
            .select_related("user")
            .prefetch_related("following", "followers")
            .annotate(
                followers_count = Count("followers"),
                following_count = Count("following")
            )
        )
    
    def get_object(self):
        return get_object_or_404(self.get_queryset())
    
    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        user = profile.user
        response = super().destroy(request, *args, **kwargs)
        user.delete()
        return  response
    

class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet)
    serializer_class = ProfileListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self): # choose which serializer to return
        if self.action == "list":
            return ProfileListSerializer
        if self.action == "retrieve":
            return ProfileDetailSerializer
        return ProfileListSerializer
    
    def get_queryset(self):
        queryset = (
            Profile.objects.prefetch_related(
                "following__following", "followers__follower"
            )
            .select_related("user")
            .annotate(
                followed_by_me = Exists (
                    FollowingRelationships.objects.filter(
                        follower__user = self.request.user, following = OuterRef("pk")
                    )
                ), 
                follower_count = Count("followers"), 
                following_count = Count("following")
            )
        )

        username = self.request.query_params.get("username")
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if username:
            queryset = queryset.filter(user__username__icontains = username)

        if first_name:
            queryset = queryset.filter(user__first_name__icontains = first_name)
        
        if last_name:
            queryset = queryset.filter(user__last_name__icontains = last_name)
        
        return queryset

    # Helps make API explainable to others 
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=OpenApiTypes.STR,
                description="Filter by username example: ?username=john",
            ),
            OpenApiParameter(
                "first_name",
                type=OpenApiTypes.STR,
                description="Filter by first name example: ?first_name=john",
            ),
            OpenApiParameter(
                "last_name",
                type=OpenApiTypes.STR,
                description="Filter by last name example: ?last_name=john",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(
        detail = True, 
        methods = ["POST"], 
        url_path = "follow", 
        permission_classes = [IsAuthenticated]
        authentication_classes = [JWTAuthentication],
    )
    def follow(self, request, pk=None):
        follower = get_object_or_404(Profile, user = request.user)
        following = get_object_or_404(Profile, pk=pk)

        if follower == following:
            return Response(
                {"detail": "You cannot follow yourself"}, 
                status = status.HTTP_400_BAD_REQUEST,
            )
        
        if FollowingRelationships.objects.filter(
            follower=follower, following=following
        ).exists():
            return Response(
                {"detail": "You are already following this user"}, 
                status = status.HTTP_409_CONFLICT,
            )
        
        FollowingRelationships.objects.create(follower=follower, following=following)
        return Response(
            {"detail": "You started following this user."}, 
            status=status.HTTP_204_NO_CONTENT,
        )
    
    @action(
        detail = True, 
        methods = ["POST"], 
        url_path = "unfollow", 
        permission_classes = [IsAuthenticated]
        authentication_classes = [JWTAuthentication],
    )
    def unfollow(self, request, pk=None):
        follower = get_object_or_404(Profile, user = request.user)
        following = get_object_or_404(Profile, pk=pk)

        try: 
            relation = FollowingRelationships.objects.get(
                Q(follower=follower) & Q(following = following)
            )
            relation.delete()
            return Response(
                {"detail": "You have unfollowed this user."}, 
                status=status.HTTP_204_NO_CONTENT,
            )
        except FollowingRelationships.DoesNotExist:
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
""" Who is this profile following """
class ProfileFollowingView(ListAPIView):
    serializer_class = FollowingRelationshipsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.profile.followers.all()
    
class TradeViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return TradeListSerializer
        if self.action == "retrieve":
            return TradeDetailSerializer
        if self.action == "upload_image":
            return TradeImageSerializer
        return TradeSerializer
    
    def get_queryset(self):
        user_profile = self.request.user.profile
        queryset = (
            Trade.objects.prefetch_related("likes__profile", "comments__author")
            .select_related("author")
            .annotate(
                likes_count = Subquery(
                    Like.objects.filter(trade=OuterRef("pk"))
                    .values("trade")
                    .annotate(cnt = Count("trade"))
                    .values("cnt")
                ), 
                comments_count = Subquery(
                    Comment.objects.filter(trade = OuterRef("pk"))
                    .values("trade")
                    .annotate(cnt = Count("trade"))
                    .values("cnt")
                ), 
                liked_by_user = Exists(
                    Like.objects.filter(profile = user_profile, trade = OuterRef("pk"))
                ),
            )
        )

        content = self.request.query__params.get("content")
        author_username = self.request.query_params.get("author_username") # USE THIS LATER

        if author_username is not None: 
            queryset = queryset.filter(author__username__icontains=author_username)
        
        if content is not None:
            queryset = queryset.filter(content__icontains=content)
        
        return content
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "content",
                type=OpenApiTypes.STR,
                description="Filter by content example: ?content=hello",
            ),
            OpenApiParameter(
                "author_username",
                type=OpenApiTypes.STR,
                description="Filter by author username example: ?author_username=john",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Endpoint to upload an image to a trade"""
        trade = get_object_or_404(Trade, pk=pk)
        trade.image = request.data.get("image")
        trade.save()
        return Response(
            {"detail": "Image uploaded successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="like",
    )
    def like(self, request, pk=None):
        """Endpoint to like a trade"""
        trade = get_object_or_404(Trade, pk=pk)
        user_profile = request.user.profile
        if Like.objects.filter(profile=user_profile, trade=trade).exists():
            return Response(
                {"detail": "You have already liked this trade."},
                status=status.HTTP_409_CONFLICT,
            )
        Like.objects.create(profile=user_profile, trade=trade)
        return Response(
            {"detail": "You liked this trade."}, status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="unlike",
    )
    def unlike(self, request, pk=None):
        """Endpoint to unlike a trade"""
        trade = get_object_or_404(Trade, pk=pk)
        user_profile = request.user.profile
        try:
            like = Like.objects.get(profile=user_profile, trade=trade)
            like.delete()
            return Response(
                {"detail": "You unliked this tradde."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Like.DoesNotExist:
            return Response(
                {"detail": "You have not liked this trade."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        methods=["GET"],
        detail=False,
        url_path="my-trade",
    )
    def my_trades(self, request):
        """Endpoint to get all trades from the user"""
        user_profile = request.user.profile
        queryset = self.get_queryset().filter(author=user_profile)
        serializer = TradeListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        url_path="feed",
    )
    def feed(self, request):
        """Endpoint to get all trades from followed users"""
        user_profile = request.user.profile
        followed_profiles = user_profile.following.values_list("following", flat=True)
        queryset = self.get_queryset().filter(author__in=followed_profiles)
        serializer = TradeListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        url_path="liked",
    )
    def liked(self, request):
        """Endpoint to get all trades liked by the user"""
        user_profile = request.user.profile
        queryset = self.get_queryset().filter(likes__profile=user_profile)
        serializer = TradeListSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.select_related("author", "trade").filter(
            trade_id=self.kwargs["trade_id"]
        )
        return queryset

    def perform_create(self, serializer):
        trade = get_object_or_404(Trade, id=self.kwargs.get("trade_id"))
        serializer.save(author=self.request.user.profile, trade=trade)