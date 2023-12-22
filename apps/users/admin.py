from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models.user import User

# Admin panel customization
admin.site.site_title = "Admin"
admin.site.site_header = "BlueWave Administration"
admin.site.index_title = "BlueWave"


@admin.register(User)
class ModelNameAdmin(BaseUserAdmin):
    """Register user admin."""
