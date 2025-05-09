from django.urls import path
from .views import *

app_name = "django_social"

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', CreatePostUser.as_view(), name='create-post'),
]