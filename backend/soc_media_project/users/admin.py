from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser

from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    form = CustomUserChangeForm

    list_display = ("username", "email", "is_staff", "is_active",)
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "birth_date", "profile_picture", "bio", "location", "interests")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "first_name", "last_name", "birth_date", "profile_picture", "bio", "location", "interests"),
        }),
    )

    search_fields = ("username", "email", "first_name", "last_name")   
    ordering = ("username",)

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
