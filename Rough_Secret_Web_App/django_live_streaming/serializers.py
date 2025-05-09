from rest_framework import serializers
from .models import (
    StreamSession,
    StreamMessage,
    StreamReaction,
    StreamGift,
    FanRelation,
    StreamWatchSession
)
from django_rest_authentication.serializer import UserSerializer


class StreamSessionSerializer(serializers.ModelSerializer):
    streamer = UserSerializer(read_only=True)

    class Meta:
        model = StreamSession
        fields = '__all__'
        read_only_fields = ['is_live', 'started_at', 'ended_at', 'stream_id']


class StreamMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = StreamMessage
        fields = '__all__'
        read_only_fields = ['sent_at']


class StreamReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StreamReaction
        fields = '__all__'
        read_only_fields = ['reacted_at']


class StreamGiftSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = StreamGift
        fields = '__all__'
        read_only_fields = ['sent_at']


class FanRelationSerializer(serializers.ModelSerializer):
    streamer = UserSerializer(read_only=True)
    fan = UserSerializer(read_only=True)

    class Meta:
        model = FanRelation
        fields = '__all__'
        read_only_fields = ['followed_at']


class StreamWatchSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StreamWatchSession
        fields = '__all__'
        read_only_fields = ['started_at', 'ended_at', 'coins_deducted']
