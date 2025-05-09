from django.contrib import admin
from .models import NotificationType, AdminNotification, Notification, AdminNotificationMapping

# NotificationType Model
@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'title', 'message', 'content')
    search_fields = ('type_name', 'title')
    list_filter = ('type_name',)

# AdminNotification Model
@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'created_on')
    search_fields = ('sender__email',)
    list_filter = ('created_on',)

# Notification Model
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'sender', 'type', 'title', 'message', 'is_read', 'created_on')
    search_fields = ('receiver__email', 'sender__email', 'title', 'message')
    list_filter = ('is_read', 'created_on')
    ordering = ('-created_on',)

# AdminNotificationMapping Model
@admin.register(AdminNotificationMapping)
class AdminNotificationMappingAdmin(admin.ModelAdmin):
    list_display = ('admin_notification', 'notification', 'is_sent')
    search_fields = ('admin_notification__id', 'notification__id')
    list_filter = ('is_sent',)
