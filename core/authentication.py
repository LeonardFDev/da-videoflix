from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CookieJWTAuthentication(JWTAuthentication):
    """uses the token through the cookie"""

    def authenticate(self, request):
        """Check if in cookie, the token exists and if it is still valid, otherwise you will see an error"""
        access_token = request.COOKIES.get("access_token")

        if access_token is None:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        except InvalidToken:
            return None