from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GroupViewSet, GroupMembershipViewSet, MessageListCreateView,
    MessageReadStatusUpdateView, UserActivityView,
    MutedUserListCreateView, MutedUserDeleteView
)

app_name = "django_chat"

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'group-memberships', GroupMembershipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/read-status/<int:pk>/', MessageReadStatusUpdateView.as_view(), name='read-status-update'),
    path('user-activity/', UserActivityView.as_view(), name='user-activity'),
    path('muted-users/', MutedUserListCreateView.as_view(), name='muted-user-list-create'),
    path('muted-users/<int:user_id>/un-mute/', MutedUserDeleteView.as_view(), name='un-mute-user'),
]