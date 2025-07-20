from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get('username')
        password = attrs.get('password')
        
        if not identifier or not password:
            raise serializers.ValidationError('Must include "username/email" and "password".')
        
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try: 
                user = User.objects.get(email=identifier)
            except User.DoesNotExist: 
                raise serializers.ValidationError('No user with given username/email')

        user = authenticate(request=self.context.get('request'), username = user.username, password = password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        data = super().validate({'username': user.username, 'password': password})
        
        data['email'] = user.email
        data['username'] = user.username

        return data
        
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs    

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

