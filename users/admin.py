from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Achievement

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'user_code', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'user_code')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Achievement)
