import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email as django_validate_email
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


def _validate_full_name(value):
    value = str(value or "").strip()

    if len(value) < 3:
        raise serializers.ValidationError(
            "Numele complet trebuie să aibă cel puțin 3 caractere."
        )

    if len(value) > 100:
        raise serializers.ValidationError(
            "Numele complet nu poate depăși 100 de caractere."
        )

    if not re.match(r"^[A-Za-zĂÂÎȘȚăâîșț\s.'-]+$", value):
        raise serializers.ValidationError(
            "Numele complet poate conține doar litere, spații, punct, apostrof sau cratimă."
        )

    return value


def _validate_username(value):
    value = str(value or "").strip()

    if len(value) < 3:
        raise serializers.ValidationError(
            "Username-ul trebuie să aibă cel puțin 3 caractere."
        )

    if len(value) > 30:
        raise serializers.ValidationError(
            "Username-ul nu poate depăși 30 de caractere."
        )

    if not re.match(r"^[A-Za-z0-9_.-]+$", value):
        raise serializers.ValidationError(
            "Username-ul poate conține doar litere, cifre, punct, underscore sau cratimă."
        )

    return value


def _validate_email(value):
    value = str(value or "").strip().lower()

    if not value:
        raise serializers.ValidationError("Emailul este obligatoriu.")

    try:
        django_validate_email(value)
    except DjangoValidationError:
        raise serializers.ValidationError("Introdu o adresă de email validă.")

    return value


def _validate_strong_password(value):
    value = str(value or "")

    try:
        validate_password(value)
    except DjangoValidationError as exc:
        raise serializers.ValidationError(list(exc.messages))

    if len(value) < 8:
        raise serializers.ValidationError(
            "Parola trebuie să aibă cel puțin 8 caractere."
        )

    if not re.search(r"[A-Z]", value):
        raise serializers.ValidationError(
            "Parola trebuie să conțină cel puțin o literă mare."
        )

    if not re.search(r"[a-z]", value):
        raise serializers.ValidationError(
            "Parola trebuie să conțină cel puțin o literă mică."
        )

    if not re.search(r"\d", value):
        raise serializers.ValidationError(
            "Parola trebuie să conțină cel puțin o cifră."
        )

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", value):
        raise serializers.ValidationError(
            "Parola trebuie să conțină cel puțin un caracter special."
        )

    return value


class RegisterClientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["full_name", "username", "email", "password"]

    def validate_full_name(self, value):
        return _validate_full_name(value)

    def validate_username(self, value):
        value = _validate_username(value)

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Există deja un utilizator cu acest username."
            )

        return value

    def validate_email(self, value):
        value = _validate_email(value)

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Există deja un utilizator cu acest email."
            )

        return value

    def validate_password(self, value):
        return _validate_strong_password(value)

    def create(self, validated_data):
        full_name = validated_data.pop("full_name").strip()

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

    def validate_full_name(self, value):
        return _validate_full_name(value)

    def validate_username(self, value):
        value = _validate_username(value)

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Există deja un utilizator cu acest username."
            )

        return value

    def validate_email(self, value):
        value = _validate_email(value)

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Există deja un utilizator cu acest email."
            )

        return value

    def validate_password(self, value):
        return _validate_strong_password(value)

    def create(self, validated_data):
        full_name = validated_data.pop("full_name").strip()

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