from django.urls import path
from .views import CreatePostUser, PostListView

app_name = "django_social"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/create/", CreatePostUser.as_view(), name="post-create"),
]