from datetime import timedelta, date

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.db import transaction
from cities_light.models import Country, Region, City
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from urllib3 import request

from .models import UserModel, UserSettings
from .utils import generate_secure_password


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']

class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["id", "name", "codename"]

class UserSerializer(serializers.ModelSerializer):

    phone = PhoneNumberField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False)
    groups = serializers.ListField(child=serializers.CharField(), required=False)
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = [
            'id', 'first_name', 'last_name', 'username', 'email', 'password', 'phone', 'gender', 'date_of_birth',
            'is_active', 'profile_picture', 'city', 'zip_code', 'state', 'country', 'is_verified',
            'is_profile_complete', 'groups'
        ]
        read_only_fields = ['is_verified']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return f"{settings.BASE_URL}{obj.profile_picture.url}"
        return None

    def get_permissions(self, instance):
        if not isinstance(instance, UserModel):
            return []
        user_permissions = set(instance.user_permissions.values_list("codename", flat=True) or [])
        group_permissions = set(instance.groups.values_list("permissions__codename", flat=True) or [])
        return list(user_permissions.union(group_permissions))

    def to_representation(self, instance):
        """Show group names in groups field."""
        rep = super().to_representation(instance)
        rep['groups'] = list(instance.groups.values_list('name', flat=True)) if instance.groups.exists() else []
        return rep

    def validate(self, data):
        """Validates user input based on various constraints."""
        email = data.get("email", "").strip().lower()
        if email:
            try:
                validate_email(email)
            except ValidationError as e:
                raise serializers.ValidationError(f"Enter a valid email address. {e.detail}")
            if UserModel.objects.filter(email=email).exclude(id=self.instance.id if self.instance else None).exists():
                raise serializers.ValidationError("A user with this email already exists.")

        phone = data.get("phone")
        if phone:
            try:
                validate_international_phonenumber(phone)
            except ValidationError as e:
                raise serializers.ValidationError(f"Enter a valid phone number. {e.detail}")
            if UserModel.objects.filter(phone=phone).exclude(id=self.instance.id if self.instance else None).exists():
                raise serializers.ValidationError("A user with this phone number already exists.")

        gender = data.get("gender")
        valid_genders = {"male", "female", "trans", "other"}
        if gender and gender not in valid_genders:
            raise serializers.ValidationError("Invalid gender choice.")

        dob = data.get("date_of_birth")
        if dob:
            if dob > date.today():
                raise serializers.ValidationError("Date of birth cannot be in the future.")
            min_age_date = date.today() - timedelta(days=18 * 365)
            if dob > min_age_date:
                raise serializers.ValidationError("User must be at least 18 years old.")

        password = data.get("password")
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                raise serializers.ValidationError(e.detail)

        for field in ["city", "state", "zip_code"]:
            value = data.get(field)
            if value and not value.replace("", "").isalnum():
                raise serializers.ValidationError(f"Invalid characters in {field}.")

        return data

    def create(self, validated_data):
        group_names = validated_data.pop("groups", [])
        password = validated_data.pop("password", None) or generate_secure_password()
        validated_data["email"] = validated_data.get("email", "").lower().strip()

        with transaction.atomic():
            user = UserModel.objects.create_user(**validated_data, password=password)
            
            if group_names:
                existing_groups = Group.objects.filter(name__in=group_names)
                existing_group_names = set(existing_groups.values_list("name", flat=True))
                missing_group_names = set(group_names) - existing_group_names

                new_groups = [Group.objects.create(name=name) for name in missing_group_names]
                all_groups = list(existing_groups) + new_groups

                user.groups.set(all_groups)
            else:
                default_group, _ = Group.objects.get_or_create(name="User")
                user.groups.add(default_group)

        return user

    def update(self, instance, validated_data):
        """Updates user details efficiently, handling password and group updates securely."""
        password = validated_data.pop('password', None)
        group_names = validated_data.pop('groups', None)

        if password:
            instance.set_password(password)

        updated_fields = []
        for field, value in validated_data.items():
            if getattr(instance, field) != value:
                setattr(instance, field, value)
                updated_fields.append(field)

        if updated_fields:
            instance.save(update_fields=updated_fields)

        if group_names is not None:
            existing_groups = Group.objects.filter(name__in=group_names)
            existing_group_names = set(existing_groups.values_list("name", flat=True))
            missing_group_names = set(group_names) - existing_group_names

            new_groups = [Group.objects.create(name=name) for name in missing_group_names]
            all_groups = list(existing_groups) + new_groups

            instance.groups.set(all_groups)

        return instance

    @staticmethod
    def get_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")
        user = authenticate(request=request, email=email, password=password)
        if not user:
            raise serializers.ValidationError(f"Invalid Credentials. {email} or {password}")

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_verified": getattr(user, "is_verified", False),
            "groups": list(user.groups.values_list("name", flat=True)) if user.groups.exists() else [],
            "permissions": self.get_user_permissions(user),
            "access_token": access_token,
            "refresh_token": str(refresh_token)
        }

    @staticmethod
    def get_user_permissions(user):
        """Fetches user permissions including group-based permissions."""
        user_permissions = set(user.user_permissions.values_list("codename", flat=True) or [])
        group_permissions = set(user.groups.values_list("permissions__codename", flat=True) or [])
        all_permissions = list(user_permissions | group_permissions)

        return [
            perm for perm in all_permissions
            if isinstance(perm, str) and perm.startswith(("add_", "view_", "change_", "delete_"))
        ]

class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSettings
        fields = "__all__"

#______________________________________________________________________________________________________________________
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code2']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'country']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'region', 'country']
