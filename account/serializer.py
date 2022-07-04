from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

from .models import CustomUser


class UserAuthenticateSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(UserAuthenticateSerializer, cls).get_token(user)
        return token

    def validate(self, user):
        data = super(UserAuthenticateSerializer, self).validate(user)
        data.update({"username": self.user.username})
        data.update({"email": self.user.email})
        return data


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


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('password', 'new_password', 'confirm_new_password')

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise serializers.ValidationError({"Validation Error": 'New password and confirm password doesn\'t '
                                                                       'match.'})
        else:
            return data

    def update(self, instance, validated_data):
        new_password = self.validated_data.pop('new_password', None)
        instance.set_password(new_password)
        instance.save()
        return instance

class UserNameChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username',)

    def validate(self, data):
        new_username = data.get('username')
        if self.Meta.model.objects.filter(username=new_username).exists():
            raise serializers.ValidationError({'Validation Error': 'Username has already been used.'})
        else:
            return data

    def update(self, instance, validated_data):
        new_username = validated_data.pop('username', None)
        instance.username = new_username
        instance.save()
        return instance


class UserEmailChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def validate(self, data):
        new_email = data.get('email')
        if self.Meta.model.objects.filter(email=new_email).exists():
            raise serializers.ValidationError({'Validation Error': 'Email has already been used.'})
        else:
            return data

    def update(self, instance, validated_data):
        new_email = validated_data.pop('email', None)
        instance.email = new_email
        instance.save()
        return instance
