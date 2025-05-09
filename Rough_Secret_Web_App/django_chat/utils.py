import os
import random
from datetime import datetime
from django.conf import settings


def get_safe_email(instance):
    """
    Extract and sanitize email for use in folder path.
    """
    email = None
    if hasattr(instance, 'sender') and instance.sender:
        email = getattr(instance.sender.user, 'email', None)
    elif hasattr(instance, 'created_by') and instance.created_by:
        email = getattr(instance.created_by.user, 'email', None)

    if not email:
        return 'unknown'

    return email.replace('@', '_at_').replace('.', '_dot_')

def save_file(instance, filename, base_dir):
    """
    Save files under a safe structure like:
    users/{email}/{base_dir}/{date}/{random_timestamped_filename}
    """
    ext = os.path.splitext(filename)[1]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    rand = f"{random.randint(0, 9999):04d}"
    safe_email = get_safe_email(instance)

    folder = f"users/{safe_email}/{base_dir}/{datetime.now().date()}"
    full_path = os.path.join(settings.MEDIA_ROOT, folder)
    os.makedirs(full_path, exist_ok=True)

    return os.path.join(folder, f"{timestamp}_{rand}{ext}")

def chat_file_upload_path(instance, filename):
    return save_file(instance, filename, "chat_files")

def group_image_upload_path(instance, filename):
    return save_file(instance, filename, "group_images")
