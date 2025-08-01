from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')
        read_only_fields = ('username', 'id', 'date_joined', 'last_login')