from django.urls import path
from .google_oauth import GoogleLoginAPIView

from users.views import (
    RegistrationAPIView,
    AuthorizationAPIView,
    ConfirmUserAPIView,
    CustomTokenObtainPairView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("registration/", RegistrationAPIView.as_view()),
    path("authorization/", AuthorizationAPIView.as_view()),
    path("confirm/", ConfirmUserAPIView.as_view()),
    path("jwt/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("google-login/", GoogleLoginAPIView.as_view()),
]
