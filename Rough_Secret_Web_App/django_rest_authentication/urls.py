from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView, TokenVerifyView)

from .views import *

app_name = "django_rest_authentication"

urlpatterns = [

    path("login-jwt/", LoginView.as_view(), name="token_obtain_pair"),
    path("logout-jwt/", LogoutView.as_view(), name="logout"),

    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path('users/active/', UserListActiveView.as_view(), name='get_users'),
    path('users/in-active/', UserListInActiveView.as_view(), name='get_users'),

    path('user/', UserListIdView.as_view(), name='get_user'),
    path('user/register/', UserRegisterView.as_view(), name='register_user'),
    path('user/verify/<str:token>/', UserVerifyView.as_view(), name='verify_user'),

    path('user/<int:id>/update/', UserUpdateView.as_view(), name='update_user'),
    path('user/<int:id>/delete/', UserDeleteView.as_view(), name='delete_user'),

    path('user/password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('user/password-forgot/', ForgotPassword.as_view(), name='password-forgot'),

    path("user/role/<int:pk>/", GroupDetailView.as_view(), name="role-detail"),
    path("user/permissions/", PermissionListView.as_view(), name="permission-list"),

    path("countries/", Countries.as_view(), name="countries"),
    path("regions/", Regions.as_view(), name="regions"),
    path("cities/", Cities.as_view(), name="cities")

]