# """URL configuration for the register, login, logout and token refresh API."""

from django.urls import path

from .views import RegistrationView, ActivateView, LoginView, LogoutView, CustomTokenRefreshView, PasswordResetView, PasswordConfirmView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_confirm/<uidb64>/<token>/', PasswordConfirmView.as_view(), name='password_confirm')
]