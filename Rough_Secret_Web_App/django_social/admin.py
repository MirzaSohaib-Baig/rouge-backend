from django.contrib import admin
from .models import Post, PostMedia, PostMention, PostTag, PostTagMapping, PostPayment, GroupEvent, EventRSVP

# ========== Post Models (User + Group Posts) ==========

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'group', 'content_preview', 'visibility', 'is_paid', 'price', 'created_at', 'updated_at')
    search_fields = ('author__username', 'group__name', 'content')
    list_filter = ('visibility', 'is_paid', 'group')

    def content_preview(self, obj):
        return obj.content[:40] if obj.content else ""
    content_preview.short_description = 'Content'

class PostMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'media_type')
    search_fields = ('post__content',)
    list_filter = ('media_type',)

class PostMentionAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'mentioned_user')
    search_fields = ('post__content', 'mentioned_user__username')

class PostTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class PostTagMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'tag')
    search_fields = ('post__content', 'tag__name')

class PostPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'paid_at')
    search_fields = ('post__content', 'user__username')

# ========== Group Event Models ==========

class GroupEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'title', 'start_time', 'end_time', 'created_at')
    search_fields = ('group__name', 'title')
    list_filter = ('group',)

class EventRSVPAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'user', 'status', 'responded_at')
    search_fields = ('event__title', 'user__username')
    list_filter = ('status', 'event')

# ========== Register Models ==========

admin.site.register(Post, PostAdmin)
admin.site.register(PostMedia, PostMediaAdmin)
admin.site.register(PostMention, PostMentionAdmin)
admin.site.register(PostTag, PostTagAdmin)
admin.site.register(PostTagMapping, PostTagMappingAdmin)
admin.site.register(PostPayment, PostPaymentAdmin)
admin.site.register(GroupEvent, GroupEventAdmin)
admin.site.register(EventRSVP, EventRSVPAdmin)
