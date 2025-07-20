from django.urls import path
from .views import MyTokenObtainPairSerializer, RegisterView

# Create your views here.
urlpatterns = [
    path('', MyTokenObtainPairSerializer.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
]