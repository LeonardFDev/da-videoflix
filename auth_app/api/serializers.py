# """Serializers for Authentication and registration operations."""

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
        """checks that both passwords entered match"""
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
        """Create the user"""
        validated_data.pop("confirmed_password")

        account = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )

        uidb64 = urlsafe_base64_encode(force_bytes(account.id))
        token = default_token_generator.make_token(account) 

        activation_link = (
            f"http://localhost:8000/api/activate/{uidb64}/{token}/"
        )

        data = {"account":account, "activation_token":token}

        queue = get_queue("default", autocommit=True)
        queue.enqueue(create_send_email, account, activation_link)

        return data


class ActivateSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        uidb64 = attrs["uidb64"]
        token = attrs["token"]

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
        except Exception:
            raise serializers.ValidationError({"detail": "Invalid activation link."})
        
        if user.is_active:
            raise serializers.ValidationError({"detail": "The user account is already activated."})

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Invalid or expired token."})

        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.is_active = True
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    """Serializer for the User login."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "username" in self.fields:
            self.fields.pop("username")


    def validate(self, attrs):
        """Check password and email and output the user if successful"""

        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")
        
        data = super().validate({"username": user.username, "password": password})
        return data


class PasswordResetSerializer(serializers.Serializer):
    # """Serializer for the User registration."""
    email = serializers.EmailField(required=True)
    
    def create(self, validated_data):
        email = validated_data["email"]
    
        try:
            account = User.objects.get(email=email, is_active=True)
        except Exception:
            raise serializers.ValidationError({"detail": "This email does not exist or has not yet been activated"})

        uidb64 = urlsafe_base64_encode(force_bytes(account.id))
        token = default_token_generator.make_token(account) 
        
        password_reset_link = (
            f"http://localhost:8000/api/password_confirm/{uidb64}/{token}/"
        )
        
        queue = get_queue("default", autocommit=True)
        queue.enqueue(password_reset_send_email, account, password_reset_link)
    
        return account


class PasswordConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_confirm_password(self, value):
        """checks that both passwords entered match"""
        new_password = self.initial_data.get('new_password')
        if new_password and value and new_password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value
    
    def validate(self, attrs):
        uidb64 = attrs["uidb64"]
        token = attrs["token"]
    
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
        except Exception:
            raise serializers.ValidationError({"detail": "Invalid activation link."})
    
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Invalid or expired token."})

        return attrs
    
    def save(self, **kwargs):
        new_password = self.validated_data["new_password"]
        uidb64 = self.validated_data["uidb64"]
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        
        user.set_password(new_password)
        user.save()
        return user