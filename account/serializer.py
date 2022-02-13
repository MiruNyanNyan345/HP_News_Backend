from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

from .models import CustomUser


class UserAuthenticateSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(UserAuthenticateSerializer, cls).get_token(user)
        return token


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data["password"]
        email = data["email"]

        # Check Email
        if self.Meta.model.objects.filter(email=email).exists():
            raise serializers.ValidationError('The email is already registered. please use another e-mail address')

        # confirm_password only used for validation
        confirm_password = data["confirm_password"]
        if not password:
            raise serializers.ValidationError('Please enter the Password!')
        if not confirm_password:
            raise serializers.ValidationError('Please confirm the Password!')
        if password != confirm_password:
            raise serializers.ValidationError('Password and Confirm-Password must match!')
        data.pop('confirm_password', None)

        # hash password
        password = data.pop('password', None)
        password = make_password(password)
        data["password"] = password

        return data

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)

        instance.save()
        return instance
