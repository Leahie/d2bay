from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, UserAPIView, DetailUserView, UserUpdateView
from rest_framework_simplejwt.views import TokenRefreshView


# Create your views here.
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserAPIView.as_view(), name='user'),
    path('user/<str:username>', DetailUserView.as_view(), name='user_details'),
    path('user/update/', UserUpdateView.as_view(), name="user_update"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), 
]