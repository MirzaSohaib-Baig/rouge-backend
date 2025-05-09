from django.db import models
from django.utils import timezone

# Predefined types for notifications
NOTIFICATION_TYPES = (
    ('message', 'Message'),
    ('profile', 'Profile'),
    ('request', 'Request'),
    ('join_group', 'Join Group'),
    ('group_request', 'Group Request'),
    ('other', 'Other'),
    ('post', 'Post'),
    ('comment', 'Comment'),
    ('birthday', 'Birthday'),
    ('post_request', 'Post Request'),
    ('group_invite', 'Group Invite'),
    ('questionnaire', 'Questionnaire'),
)

class NotificationType(models.Model):

    type_name = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    content = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Notification Type"
        verbose_name_plural = "Notification Types"

    def __str__(self):
        return self.type_name


class AdminNotification(models.Model):

    sender = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE, related_name="admin_notifications")
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Admin Notification"
        verbose_name_plural = "Admin Notifications"

    def __str__(self):
        return f"AdminNotification by {self.sender.get_full_name()} at {self.created_on}"


class Notification(models.Model):

    receiver = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE, related_name="notifications_received")
    sender = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE, null=True, blank=True, default=None,
        related_name="notifications_sent")
    type = models.ForeignKey(NotificationType, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")

    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    action_required = models.BooleanField(default=False)
    content = models.JSONField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_on']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"To {self.receiver.get_full_name()}: {self.message[:30]}"


class AdminNotificationMapping(models.Model):

    admin_notification = models.ForeignKey(AdminNotification, on_delete=models.CASCADE, related_name="mappings")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="admin_mappings")
    is_sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Admin Notification Mapping"
        verbose_name_plural = "Admin Notification Mappings"
        unique_together = ('admin_notification', 'notification')

    def __str__(self):
        return f"AdminNotif {self.admin_notification_id} -> Notif {self.notification_id}"
