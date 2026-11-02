"""registration, activate account, login, logout, reset password and confirm new password API views."""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from datetime import timedelta
from django_rq import get_queue

from .serializers import RegistrationSerializer, ActivateSerializer, LoginSerializer, PasswordResetSerializer, PasswordConfirmSerializer
from services.tasks.delete_unactivated_user import delete_unactivated_user


def blacklist_old_refresh_token(request):
    """Blacklist the refresh token"""

    refresh = request.COOKIES.get("refresh_token")

    if refresh:
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            pass


class RegistrationView(APIView):
    """Provides an API endpoint for user registration."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user."""

        blacklist_old_refresh_token(request)
        
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.save()

            queue = get_queue("default", autocommit=True)
            queue.enqueue_in(timedelta(minutes=15), delete_unactivated_user, data["account"].id)

            data = {
                "user":{
                    "id": data["account"].id,
                    "email": data["account"].email
                },
                "token": data["activation_token"]
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):
    """Provides an API endpoint to activate the user account."""

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        """Activate the user"""
        serializer = ActivateSerializer(data={"uidb64": uidb64,"token": token})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {"message": "Account successfully activated."}

        return Response(data, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    """Provides an API endpoint for user login."""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Authenticate the user and sets the tokens in cookie and outputs a confirmation as well as the user information"""
        blacklist_old_refresh_token(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
            
        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        user = serializer.user
        user_data = {"id": user.id, "email": user.email}

        response = Response({"detail": "Login successful", "user": user_data})

        response.set_cookie(
            key="access_token",
            value= access,
            httponly= True,
            secure= True,
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value= refresh,
            httponly= True,
            secure= True,
            samesite="Lax"
        )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    """Provides an API endpoint for token refresh"""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """A new access token is created with the refresh token"""
        refresh_token = request.COOKIES.get("refresh_token")

        self.no_refresh_token_error(refresh_token)

        return self.update_access_token(refresh_token)

    def no_refresh_token_error(self, refresh_token):
        """Error creating a new token because there is no refresh token"""
        if refresh_token is None:
            raise ValidationError("Refresh token not found!")

    def update_access_token(self, refresh_token):
        """Try to generate a new access token"""
        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            self.refresh_token_invalid_error()

        return self.update_token_cookie(serializer)

    def refresh_token_invalid_error(self):
        """Error message that the refresh token is no longer valid"""
        raise NotAuthenticated("Refresh token invalid!")

    def update_token_cookie(self, serializer):
        """Inserts the newly generated access token into the cookie"""
        access_token = serializer.validated_data.get("access")

        data = {
            "detail": "Token refreshed",
            "access": access_token
        }

        response = Response(data)
        
        response.set_cookie(
            key="access_token",
            value= access_token,
            httponly= True,
            secure= True,
            samesite="Lax"
        )

        return response


class LogoutView(APIView):
    """Provides an API endpoint for logout"""

    def post(self, request):
        """Blacklists the refresh_token and deletes the tokens from the cookies"""
        blacklist_old_refresh_token(request)

        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."})

        response.delete_cookie(
            key="access_token",
            samesite="Lax"
        )

        response.delete_cookie(
            key="refresh_token",
            samesite="Lax"
        )

        return response


class PasswordResetView(APIView):
    """Provides an API endpoint to reset the password."""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Reset the password."""
        blacklist_old_refresh_token(request)
    
        serializer = PasswordResetSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
    
            data = {"detail": "An email has been sent to reset your password."}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordConfirmView(APIView):
    """Provides an API endpoint to confirm the new password."""

    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        """Create a new password"""
        data = request.data
        data["uidb64"]= uidb64
        data["token"]= token
        serializer = PasswordConfirmSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {"detail": "Your Password has been successfully reset."}

        return Response(data, status=status.HTTP_200_OK)