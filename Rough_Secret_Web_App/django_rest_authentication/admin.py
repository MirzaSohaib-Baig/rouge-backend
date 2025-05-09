from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel, UserSettings

@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    model = UserModel
    list_display = ('email', 'username', 'is_verified', 'is_profile_complete', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'phone')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'phone', 'gender', 'date_of_birth', 'height', 'weight', 'zip_code', 'city', 'state', 'country', 'bio', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'is_profile_complete', 'groups', 'user_permissions')}),
        ('Other', {'fields': ('hidden_regions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_verified', 'is_profile_complete', 'is_staff', 'is_superuser')}
        ),
    )

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_payment_req', 'is_verification_req')
    search_fields = ('user__email',)
