import os


def get_filename(instance, filename):
    if hasattr(instance, "username"):
        username = instance.username
        return os.path.join("images", username, "thumbnails", filename)
    else:
        username = instance.user.username
        return os.path.join("images", username, filename)
