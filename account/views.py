from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import UserAuthenticateSerializer, UserCreateSerializer, UserPasswordChangeSerializer, \
    UserNameChangeSerializer, UserEmailChangeSerializer


# Login; Get Token
class UserLogin(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserAuthenticateSerializer


# Register; Create User
class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordChange(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if not request.user.is_anonymous:
            request.data['email'] = request.user.email
        serializer = UserPasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Password Updated', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserNameChange(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = UserNameChangeSerializer(data=request.data, user=request.user)
        if serializer.is_valid():
            serializer.update(instance=request.user, data=request.data)
            return Response('Username Updated', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEmailChange(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = UserEmailChangeSerializer(data=request.data, user=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response('Email Updated', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
