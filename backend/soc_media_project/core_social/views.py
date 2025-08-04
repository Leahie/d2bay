from django.shortcuts import render
from rest_framework.generics import (
    get_object_or_404,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
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
from core_social.permissions import IsAuthorOr # should I add or should I just use general permissions
# Create your views here.
class CurrentUserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = Profile