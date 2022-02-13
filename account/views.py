from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import UserAuthenticateSerializer, UserCreateSerializer


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