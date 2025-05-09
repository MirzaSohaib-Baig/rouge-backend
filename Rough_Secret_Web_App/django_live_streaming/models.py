from django.db import models
from .utils import *


class StreamSession(models.Model):

    STREAM_ACCESS_CHOICES = [ ('public', 'Public'), ('fans', 'Fans Only')]

    streamer = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE, related_name='live_streams')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    access_type = models.CharField(max_length=10, choices=STREAM_ACCESS_CHOICES, default='public')
    is_live = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    saved_video = models.FileField(upload_to=user_stream_recordings_path, null=True, blank=True)

    def __str__(self):
        return f"{self.streamer.username} - {self.title} ({self.access_type})"

class StreamMessage(models.Model):

    stream = models.ForeignKey(StreamSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}"

class StreamReaction(models.Model):

    REACTION_CHOICES = [('like', 'Like'), ('dislike', 'Dislike')]

    stream = models.ForeignKey(StreamSession, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    reacted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('stream', 'user')

    def __str__(self):
        return f"{self.user.username} {self.reaction}d"

class StreamGift(models.Model):

    stream = models.ForeignKey(StreamSession, on_delete=models.CASCADE, related_name='gifts')
    sender = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} sent {self.amount} coins"

class FanRelation(models.Model):

    streamer = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE, related_name='my_fans')
    fan = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE, related_name='following_streamers')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('streamer', 'fan')

    def __str__(self):
        return f"{self.fan.username} is a fan of {self.streamer.username}"

class StreamWatchSession(models.Model):

    user = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE)
    stream = models.ForeignKey(StreamSession, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    coins_deducted = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} watched {self.stream.title}"