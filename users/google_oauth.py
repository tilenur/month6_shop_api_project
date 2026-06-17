import os  # Access environment variables
import requests  # Send HTTP requests

from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import OauthCodeSerializer

# Get active user model
CustomUser = get_user_model()


class GoogleLoginAPIView(CreateAPIView):
    # Validate incoming authorization code
    serializer_class = OauthCodeSerializer

    def post(self, request):
        # Validate request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract Google authorization code
        code = serializer.validated_data["code"]

        # Exchange code for Google access token
        token_response = requests.post(
            url="https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
                "grant_type": "authorization_code",
            },
        )

        # Convert response to dictionary
        token_data = token_response.json()

        # Get access token
        access_token = token_data.get("access_token")

        # Stop if token not received
        if not access_token:
            return Response({"error": "Invalid access token!"}, status=400)

        # Request user information from Google
        user_info = requests.get(
            url="https://www.googleapis.com/oauth2/v3/userinfo",
            params={"alt": "json"},
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()

        # Print user data for debugging
        print("user_info", user_info)

        # Extract email from Google profile
        email = user_info["email"]

        # Find existing user or create new one
        user, created = CustomUser.objects.get_or_create(
            email=email,
        )

        # Generate JWT refresh token
        refresh = RefreshToken.for_user(user)

        # Add custom claim
        refresh["email"] = user.email

        # Return JWT tokens
        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }
        )
