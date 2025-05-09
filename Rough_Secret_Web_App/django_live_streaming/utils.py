import os
from datetime import datetime


def user_stream_recordings_path(instance, filename):
    """
    Upload path: users/{email}/profile_pictures/{timestamped_filename}
    """
    # Fallback if no email is set
    email = getattr(instance, 'email', None)
    if not email:
        return os.path.join('users/unknown/stream_recordings/', filename)

    # Sanitize email for use in path (optional, but recommended)
    safe_email = email.replace('@', '_at_').replace('.', '_dot_')

    # Timestamped filename
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"profile_{timestamp}.{ext}"

    return os.path.join(f'users/{safe_email}/stream_recordings/', filename)
