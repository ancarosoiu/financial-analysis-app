from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Company

User = get_user_model()


class RegisterClientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["full_name", "username", "email", "password"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Există deja un utilizator cu acest username.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Există deja un utilizator cu acest email.")
        return value

    def create(self, validated_data):
        full_name = validated_data.pop("full_name")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=full_name,
            role=User.CLIENT,
        )

        return user


class RegisterAnalystSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["full_name", "username", "email", "password"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Există deja un utilizator cu acest username.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Există deja un utilizator cu acest email.")
        return value

    def create(self, validated_data):
        full_name = validated_data.pop("full_name")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=full_name,
            role=User.ANALYST,
        )

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data["username"] = user.username
        data["role"] = user.role

        company = getattr(user, "company", None)

        if user.role == User.CLIENT and company:
            data["is_onboarded"] = company.is_onboarded
            data["company_id"] = company.id
        else:
            data["is_onboarded"] = True if user.role == User.ANALYST else False
            data["company_id"] = None

        return data