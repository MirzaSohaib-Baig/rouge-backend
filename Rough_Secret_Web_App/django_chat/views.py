from rest_framework import viewsets, permissions, generics
from .models import *
from .serializers import *

class GroupViewSet(viewsets.ModelViewSet):

    queryset = GroupDetail.objects.all()
    serializer_class = GroupDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        # print("User:", self.request.user)
        # print("User ID:", self.request.user.id)
        # print("User Groups:", self.queryset.filter(memberships__member=self.request.user))
        return GroupDetail.objects.filter(memberships__member=self.request.user).distinct()

class GroupMembershipViewSet(viewsets.ModelViewSet):

    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class MessageListCreateView(generics.ListCreateAPIView):

    serializer_class = MessageSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        group_id = self.request.query_params.get('group')
        user = self.request.user
        if group_id:
            return Message.objects.filter(group_id=group_id)
        return Message.objects.filter(
            (models.Q(sender=user) & models.Q(type='private')) |
            (models.Q(recipient=user) & models.Q(type='private'))
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageReadStatusUpdateView(generics.UpdateAPIView):

    queryset = MessageReadStatus.objects.all()
    serializer_class = MessageReadStatusSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def perform_update(self, serializer):
        serializer.save(read=True, read_at=timezone.now())

class UserActivityView(generics.RetrieveUpdateAPIView):

    serializer_class = UserActivitySerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return UserActivity.objects.get_or_create(profile=self.request.user)[0]

class MutedUserListCreateView(generics.ListCreateAPIView):
    serializer_class = MutedUserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return MutedUser.objects.filter(muted_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(muted_by=self.request.user)

class MutedUserDeleteView(generics.DestroyAPIView):

    serializer_class = MutedUserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return MutedUser.objects.get(
            muted_by=self.request.user,
            muted_user_id=self.kwargs['user_id']
        )
