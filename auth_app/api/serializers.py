"""Serializers for registration, activate account, login, logout, reset password and confirm new password"""

import os

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator 
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django_rq import get_queue
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from services.tasks.create_confirm_email import create_send_email
from services.tasks.create_password_reset_email import password_reset_send_email


User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for the User registration."""

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate_confirmed_password(self, value):
        """Checks that both passwords entered match"""
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_email(self, value):
        """Ensures that an email exists only once"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def create(self, validated_data):
        """Initialization of Create User"""
        created_account = self.create_account(validated_data)
        uidb64 = urlsafe_base64_encode(force_bytes(created_account.id))
        token = default_token_generator.make_token(created_account)

        frontend_activate_account_url = os.environ.get("FRONTEND_ACTIVATE_ACCOUNT_URL")
        activation_link = f"{frontend_activate_account_url}?uid={uidb64}&token={token}"

        data = {"account":created_account, "activation_token":token}

        queue = get_queue("default", autocommit=True)
        queue.enqueue(create_send_email, created_account, activation_link)

        return data

    def create_account(self, validated_data):
        """Create and return the user"""
        validated_data.pop("confirmed_password")
        
        account = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )

        return account


class ActivateSerializer(serializers.Serializer):
    """Serializer for the activate user account."""

    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        """Checks if the id and token are valid"""
        uidb64 = attrs["uidb64"]
        token = attrs["token"]

        user = self.return_user_or_invalid_activation_link(uidb64)

        self.is_already_activated(user)

        self.invalid_or_expired_token(user, token)

        attrs["user"] = user
        return attrs

    def return_user_or_invalid_activation_link(self, uidb64):
        """Return the user or raise a validation error of an invalid activation link"""
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            return user
        except Exception:
            raise serializers.ValidationError({"detail": "Invalid activation link."})

    def is_already_activated(self, user):
        """If the user has already been activated, a validation error is raised"""
        if user.is_active:
            raise serializers.ValidationError({"detail": "The user account is already activated."})

    def invalid_or_expired_token(self, user, token):
        """If the token is invalid or expired, a validation error is raised"""
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Invalid or expired token."})

    def save(self, **kwargs):
        """Activates the user and saves it"""
        user = self.validated_data["user"]
        user.is_active = True
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    """Serializer for the User login."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        """Remove username field"""
        super().__init__(*args, **kwargs)

        if "username" in self.fields:
            self.fields.pop("username")

    def validate(self, attrs):
        """Check password and email and output the user if successful"""

        email = attrs.get("email")
        password = attrs.get("password")

        user = self.return_user_or_invalid_email(email)
        self.invalid_password(user, password)
        
        data = super().validate({"username": user.username, "password": password})
        return data

    def return_user_or_invalid_email(self, email):
        """Return the user or raise a validation error of an invalid email"""
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

    def invalid_password(self, user, password):
        """raise a validation error of an invalid password"""
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")


class PasswordResetSerializer(serializers.Serializer):
    """Serializer to reset the user's password."""

    email = serializers.EmailField(required=True)
    
    def create(self, validated_data):
        """Create an email to reset the password"""

        account = self.return_user_or_email_not_exist_or_not_activated(validated_data)
        uidb64 = urlsafe_base64_encode(force_bytes(account.id))
        token = default_token_generator.make_token(account)

        frontend_confirm_password_url = os.environ.get("FRONTEND_CONFIRM_PASSWORD_URL")
        password_reset_link = f"{frontend_confirm_password_url}?uid={uidb64}&token={token}"
        
        queue = get_queue("default", autocommit=True)
        queue.enqueue(password_reset_send_email, account, password_reset_link)
    
        return account

    def return_user_or_email_not_exist_or_not_activated(self, validated_data):
        """Return the user or raise a validation error of a non-existent or activated email"""
        email = validated_data["email"]

        try:
            account = User.objects.get(email=email, is_active=True)
            return account
        except Exception:
            raise serializers.ValidationError({"detail": "This email does not exist or has not yet been activated"})


class PasswordConfirmSerializer(serializers.Serializer):
    """Serializer to confirm the user's new password."""

    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_confirm_password(self, value):
        """Checks that both passwords entered match"""
        new_password = self.initial_data.get('new_password')
        if new_password and value and new_password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value
    
    def validate(self, attrs):
        """Checks if the id and token are valid"""
        user = self.return_user_or_invalid_activation_link(attrs)
        self.invalid_or_expired_token(user, attrs)

        return attrs

    def return_user_or_invalid_activation_link(self, attrs):
        """Return the user or raise a validation error of an invalid activation link"""
        uidb64 = attrs["uidb64"]

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            return user
        except Exception:
            raise serializers.ValidationError({"detail": "Invalid activation link."})

    def invalid_or_expired_token(self, user, attrs):
        """If the token is invalid or expired, a validation error is raised"""
        token = attrs["token"]

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Invalid or expired token."})
    
    def save(self, **kwargs):
        """Save new password"""
        new_password = self.validated_data["new_password"]
        uidb64 = self.validated_data["uidb64"]
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        
        user.set_password(new_password)
        user.save()
        return user