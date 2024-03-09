from django.contrib.auth import decorators


def permission_required(perm, raise_exception=True):
    """Check request's user permissions."""
    return decorators.permission_required(
        perm,
        raise_exception=raise_exception,
    )
