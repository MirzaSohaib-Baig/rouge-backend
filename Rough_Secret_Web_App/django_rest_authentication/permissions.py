from rest_framework.permissions import BasePermission


class BaseRolePermission(BasePermission):
    """
    Base permission class to check if the user is authenticated, belongs to specific groups,
    and is linked to an active client.
    """
    allowed_groups = []

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.groups.filter(name__in=self.allowed_groups).exists()

class IsAdmin(BaseRolePermission):
    """
    Grants access only to Admins.
    """
    allowed_groups = ["Admin"]

class IsStreamer(BaseRolePermission):
    """
    Grants access only to Streamers.
    """
    allowed_groups = ["Streamer"]

class IsFan(BaseRolePermission):
    """
    Grants access only to Fans.
    """
    allowed_groups = ["Fan"]

class IsUser(BaseRolePermission):
    """
    Grants access only to Users.
    """
    allowed_groups = ["User"]


class IsAdminOrIsStreamerOrIsFan(BaseRolePermission):
    """
    Grants access to "Admins", "Streamers", "Fans".
    """
    allowed_groups = ["Admin", "Streamer", "Fan"]

class IsAdminOrIsStreamerOrIsFanOrIsUser(BaseRolePermission):
    """
    Grants access to "Admins", "Streamers", "Fans",  "Users".
    """
    allowed_groups = ["Admin", "Streamer", "Fan", "User"]
