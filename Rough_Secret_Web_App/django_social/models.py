from django.db import models

POST_VISIBILITY = (
    ('public', 'Public'),
    ('private', 'Private'),
)

POST_MEDIA_TYPES = (
    ('image', 'Image'),
    ('video', 'Video'),
)

RSVP_STATUS = (
    ('going', 'Going'),
    ('interested', 'Interested'),
    ('not_going', 'Not Going'),
)

# ========== POST MODELS (Unified for User + Group) ==========

class Post(models.Model):

    author = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey('django_chat.GroupDetail', on_delete=models.CASCADE, related_name='group_posts', null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    visibility = models.CharField(max_length=10, choices=POST_VISIBILITY, default='public')
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']

    def __str__(self):
        if self.group:
            return f"{self.author.get_full_name()} (Group: {self.group.name}) - {self.content[:40]}"
        return f"{self.author.get_full_name()} - {self.content[:40]}"

class PostMedia(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to="posts/media/")
    media_type = models.CharField(max_length=10, choices=POST_MEDIA_TYPES)

    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Media for post {self.post.id}"

class PostMention(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='mentions')
    mentioned_user = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE, related_name='mentioned_in_posts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'mentioned_user')
        db_table = 'post_mentions'

    def __str__(self):
        return f"{self.mentioned_user.get_full_name()} mentioned in post {self.post.id}"

class PostTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.name}"

class PostTagMapping(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(PostTag, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'tag')
        db_table = 'post_tags'

    def __str__(self):
        return f"#{self.tag.name} on post {self.post.id}"

class PostPayment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE)
    paid_at = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'user')
        db_table = 'post_payments'

    def __str__(self):
        return f"{self.user.get_full_name()} paid for post {self.post.id}"

class PostList(models.Model):

    name = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class PostListMapping(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='lists')
    list = models.ForeignKey(PostList, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'list')
        db_table = 'post_lists'

    def __str__(self):
        return f"{self.list.name} on post {self.post.id}"

# ========== GROUP EVENT MODELS ==========

class GroupEvent(models.Model):

    group = models.ForeignKey('django_chat.GroupDetail', on_delete=models.CASCADE, related_name='events')
    created_by = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'group_events'
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.title} in {self.group.name}"

class EventRSVP(models.Model):

    event = models.ForeignKey(GroupEvent, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey('django_rest_authentication.UserModel', on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=RSVP_STATUS)
    responded_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'user')
        db_table = 'group_event_rsvps'

    def __str__(self):
        return f"{self.user.get_full_name()} RSVP {self.status} for {self.event.title}"
