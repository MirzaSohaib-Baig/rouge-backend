from rest_framework import serializers
from .models import (
    GroupDetail,
    GroupMembership,
    Message,
    MessageReadStatus,
    UserActivity,
    MutedUser
)
from django_rest_authentication.serializers import UserSerializer


# ========== GROUP SERIALIZERS ==========

class GroupDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    group_image_url = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()

    class Meta:
        model = GroupDetail
        fields = [
            'id', 'name', 'type', 'group_image', 'group_image_url',
            'created_by', 'created_at', 'group_name'
        ]

    def get_group_image_url(self, obj):
        return obj.get_group_image()

    def get_group_name(self, obj):
        return obj.get_group_name()


class GroupMembershipSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)
    group = GroupDetailSerializer(read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'group', 'member', 'joined_at']


# ========== MESSAGE SERIALIZERS ==========

class MessageReadStatusSerializer(serializers.ModelSerializer):
    reader = UserSerializer(read_only=True)

    class Meta:
        model = MessageReadStatus
        fields = ['id', 'message', 'reader', 'read', 'read_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    read_by = MessageReadStatusSerializer(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id', 'group', 'sender', 'recipient', 'content',
            'file', 'file_url', 'type', 'language', 'reel_id',
            'video_type', 'has_media', 'created_at', 'read_by'
        ]

    def get_file_url(self, obj):
        return obj.file.url if obj.file else None


# ========== USER STATE SERIALIZERS ==========

class UserActivitySerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True)
    connected_with = UserSerializer(read_only=True)

    class Meta:
        model = UserActivity
        fields = ['id', 'profile', 'connected_with', 'last_seen']


class MutedUserSerializer(serializers.ModelSerializer):
    muted_by = UserSerializer(read_only=True)
    muted_user = UserSerializer(read_only=True)

    class Meta:
        model = MutedUser
        fields = ['id', 'muted_by', 'muted_user', 'muted_on']