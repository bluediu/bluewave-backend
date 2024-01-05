from pathlib import Path

from django.utils.crypto import get_random_string
from django.utils.timezone import now


def clean_spaces(content: str) -> str:
    """Remove spaces from a string."""
    return " ".join(content.split())


# noinspection PyUnusedLocal
def image_file_path(instance, filename) -> str:
    """Return a standard image path format."""
    ext = Path(filename).suffix
    filename = f"{now().strftime('%Y%m%d%H%M%S')}_{get_random_string(4)}{ext}"
    return f"products/categories/{filename}"
