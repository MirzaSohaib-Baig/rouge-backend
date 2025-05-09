import os
import secrets
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import AccessToken


# User
def generate_secure_password():
    return secrets.token_urlsafe(12)

def user_profile_picture_path(instance, filename):
    """
    Upload path: users/{email}/profile_pictures/{timestamped_filename}
    """
    # Fallback if no email is set
    email = getattr(instance, 'email', None)
    if not email:
        return os.path.join('users/unknown/profile_pictures/', filename)

    # Sanitize email for use in path (optional, but recommended)
    safe_email = email.replace('@', '_at_').replace('.', '_dot_')

    # Timestamped filename
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"profile_{timestamp}.{ext}"

    return os.path.join(f'users/{safe_email}/profile_pictures/', filename)

def generate_email_verification_token(user):
    token = AccessToken.for_user(user)
    return str(token)

def send_verification_email(user):
    token = generate_email_verification_token(user)
    verification_url = f"{settings.BASE_URL}auth/user/verify/{token}/"
    logo_url = f"{settings.BASE_URL}media/images/logo.jpeg"

    subject = "Verify Your Email"
    html_message = render_to_string("auth/email_verification.html", {
        "full_name": user.get_full_name(),
        "verification_url": verification_url,
        "logo_url": logo_url,
        "year": datetime.now().year,
    })

    send_mail(
        subject,
        "",
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=html_message
    )

def send_password_reset_email(user, new_password):

    subject = "Your Password Is Changed"

    html_message = render_to_string("auth/password_change.html", {
        "full_name": user.get_full_name(),
        "password": new_password,
        "year": datetime.now().year,
    })

    send_mail(
        subject,
        "",
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=html_message
    )
