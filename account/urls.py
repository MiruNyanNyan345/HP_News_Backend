from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import UserCreate, UserLogin, UserPasswordChange

urlpatterns = [
    path('register/', UserCreate.as_view(), name='create_user'),
    path('token/obtain/', UserLogin.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/change_password/', UserPasswordChange.as_view(), name='change_password'),
]