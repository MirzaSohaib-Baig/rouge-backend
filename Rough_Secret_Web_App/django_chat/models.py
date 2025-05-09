from django.db import models
from django.utils import timezone
from .utils import save_file, chat_file_upload_path, group_image_upload_path


# Group Type
GROUP_TYPES = (
    ('public', 'Public'),
    ('private', 'Private'),
    ('chat', 'Chat')
)

# ========== GROUP MODELS ==========

class GroupDetail(models.Model):

    name = models.CharField(max_length=255)
    created_by = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.SET_NULL, null=True, related_name='created_groups')
    type = models.CharField(max_length=10, choices=GROUP_TYPES, default='private')
    group_image = models.FileField(upload_to=group_image_upload_path, null=True, blank=True)

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'group_detail'

    def __str__(self):
        return self.name

    def get_group_name(self):
        return self.name if self.type == 'group' else self.created_by.get_full_name()

    def get_group_image(self):
        if self.type == 'group' and self.group_image:
            return self.group_image.url
        return self.created_by.profile_picture

class GroupMembership(models.Model):

    group = models.ForeignKey(GroupDetail, on_delete=models.CASCADE, related_name='memberships')
    member = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('group', 'member')
        db_table = 'group_membership'

    def __str__(self):
        return f"{self.member.get_full_name()} in {self.group.name}"

# ========== MESSAGE MODELS ==========

class Message(models.Model):

    group = models.ForeignKey(GroupDetail, on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    sender = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    recipient = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.SET_NULL, null=True, blank=True, related_name='received_messages')

    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=chat_file_upload_path, null=True, blank=True)
    type = models.CharField(max_length=10, choices=GROUP_TYPES)
    language = models.CharField(max_length=10, default='en')
    reel_id = models.IntegerField(null=True, blank=True)
    video_type = models.CharField(max_length=100, null=True, blank=True)

    has_media = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return f"Message by {self.sender} - {self.content[:30]}"

    def get_status_for(self, user):
        return self.read_by.filter(reader=user).first().read if self.read_by.filter(reader=user).exists() else False

class MessageReadStatus(models.Model):

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="read_by")
    reader = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE)

    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'message_read_status'
        unique_together = ('message', 'reader')

    def __str__(self):
        return f"{self.reader.get_full_name()} read: {self.read}"

# ========== USER STATE MODELS ==========

class UserActivity(models.Model):

    profile = models.OneToOneField('django_rest_authentication.UserModel', on_delete=models.CASCADE, related_name='activity')
    connected_with = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.SET_NULL, null=True, blank=True, related_name='connected_users')

    last_seen = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_activity'

    def __str__(self):
        return f"{self.profile.get_full_name()} last seen: {self.last_seen}"

class MutedUser(models.Model):

    muted_by = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE, related_name="muted_by")
    muted_user = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE, related_name="muted_user")

    muted_on = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'muted_users'
        unique_together = ('muted_by', 'muted_user')

    def __str__(self):
        return f"{self.muted_by.get_full_name()} muted {self.muted_user.get_full_name()}"

# ========== CALLER LOGS ==========
class CallLogs(models.Model):

    caller = models.ForeignKey('django_rest_authentication.UserModel', related_name='outgoing_calls', on_delete=models.CASCADE)
    receiver = models.ForeignKey('django_rest_authentication.UserModel', related_name='incoming_calls', on_delete=models.CASCADE)
    room = models.CharField(max_length=255)

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Caller {self.caller} - Receiver {self.receiver} - Room {self.room}"