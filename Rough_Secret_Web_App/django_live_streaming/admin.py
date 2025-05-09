from django.contrib import admin
from .models import (
    StreamSession,
    StreamMessage,
    StreamReaction,
    StreamGift,
    FanRelation,
    StreamWatchSession
)

@admin.register(StreamSession)
class StreamSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'streamer', 'title', 'access_type', 'is_live', 'started_at', 'ended_at')
    search_fields = ('title', 'streamer__email')
    list_filter = ('access_type', 'is_live')
    date_hierarchy = 'started_at'

@admin.register(StreamMessage)
class StreamMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'stream', 'sender', 'message', 'sent_at')
    search_fields = ('message', 'sender__email')
    list_filter = ('sent_at',)

@admin.register(StreamReaction)
class StreamReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'stream', 'user', 'reaction', 'reacted_at')
    list_filter = ('reaction',)
    search_fields = ('user__email',)

@admin.register(StreamGift)
class StreamGiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'stream', 'sender', 'amount', 'sent_at')
    search_fields = ('sender__email',)
    list_filter = ('sent_at',)

@admin.register(FanRelation)
class FanRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'streamer', 'fan', 'followed_at')
    search_fields = ('streamer__email', 'fan__email')
    list_filter = ('followed_at',)

@admin.register(StreamWatchSession)
class StreamWatchSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stream', 'started_at', 'ended_at', 'coins_deducted')
    search_fields = ('user__email',)
    list_filter = ('started_at',)
