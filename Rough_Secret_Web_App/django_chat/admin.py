from django.contrib import admin
from .models import GroupDetail, GroupMembership, Message, MessageReadStatus, UserActivity, MutedUser, CallLogs

# Group Models
@admin.register(GroupDetail)
class GroupDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'type', 'created_at', 'get_group_name', 'get_group_image')
    list_filter = ('type',)
    search_fields = ('name', 'created_by__email')

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('group', 'member', 'joined_at')
    search_fields = ('group__name', 'member__email')

# Message Models
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'sender', 'recipient', 'content', 'type', 'language', 'created_at')
    list_filter = ('type', 'language')
    search_fields = ('content', 'sender__email', 'recipient__email')

@admin.register(MessageReadStatus)
class MessageReadStatusAdmin(admin.ModelAdmin):
    list_display = ('message', 'reader', 'read', 'read_at')
    search_fields = ('message__sender__email', 'reader__email')

# User Activity Models
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('profile', 'connected_with', 'last_seen')
    search_fields = ('profile__email', 'connected_with__email')

# Muted User Models
@admin.register(MutedUser)
class MutedUserAdmin(admin.ModelAdmin):
    list_display = ('muted_by', 'muted_user', 'muted_on')
    search_fields = ('muted_by__email', 'muted_user__email')

# Call Models
@admin.register(CallLogs)
class CallAdmin(admin.ModelAdmin):
    list_display = ('caller', 'receiver', 'room', 'start_time', 'end_time')
    search_fields = ('caller__email', 'receiver__email', 'room')
