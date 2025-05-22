from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_verified")
    list_filter = ("is_staff", "is_superuser", "is_verified", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Profile", {"fields": ("bio", "profile_picture", "date_of_birth")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "is_verified", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("email", "username")
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.site_header = "Instagram Admin"
admin.site.site_title = "Instagram Admin Portal"
admin.site.index_title = "Welcome to Instagram Admin"