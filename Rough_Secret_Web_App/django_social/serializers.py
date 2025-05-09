from django_rest_authentication.models import UserModel
from rest_framework import serializers

from .models import (
    Post, PostMedia, PostMention, PostTag, PostTagMapping, PostPayment,
    GroupEvent, EventRSVP
)


# ========== POST SERIALIZERS ==========

class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['id', 'file', 'media_type']


class PostMentionSerializer(serializers.ModelSerializer):

    mentioned_user_id = serializers.PrimaryKeyRelatedField(source='mentioned_user', queryset=UserModel.objects.all())
    mentioned_user_name = serializers.CharField(source='mentioned_user.get_full_name', read_only=True)

    class Meta:
        model = PostMention
        fields = ['id', 'mentioned_user_id', 'mentioned_user_name']


class PostTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostTag
        fields = ['id', 'name']


class PostTagMappingSerializer(serializers.ModelSerializer):

    tag = PostTagSerializer()

    class Meta:
        model = PostTagMapping
        fields = ['id', 'tag']


class PostPaymentSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = PostPayment
        fields = ['id', 'user', 'user_name', 'paid_at']


class PostSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    media = PostMediaSerializer(many=True, read_only=True)
    mentions = PostMentionSerializer(many=True, read_only=True)
    tags = PostTagMappingSerializer(many=True, read_only=True)
    payments = PostPaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_name', 'group', 'group_name',
            'content', 'visibility', 'is_paid', 'price',
            'created_at', 'updated_at',
            'media', 'mentions', 'tags', 'payments',
        ]


# ========== GROUP EVENT SERIALIZERS ==========

class EventRSVPSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = EventRSVP
        fields = ['id', 'event', 'user', 'user_name', 'status', 'responded_at']


class GroupEventSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    rsvps = EventRSVPSerializer(many=True, read_only=True)

    class Meta:
        model = GroupEvent
        fields = [
            'id', 'group', 'group_name', 'created_by', 'created_by_name',
            'title', 'description', 'location', 'start_time', 'end_time',
            'created_at', 'rsvps',
        ]
