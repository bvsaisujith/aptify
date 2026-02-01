from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Achievement, Goal, Course, CourseResource, CourseEnrollment


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0
    fields = ('name', 'deadline', 'status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, GoalInline)
    list_display = ('username', 'email', 'user_code', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'user_code')
    ordering = ('email',)


class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'deadline', 'status', 'created_at')
    list_filter = ('status', 'deadline', 'created_at')
    search_fields = ('name', 'user__username', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Goal Information', {
            'fields': ('user', 'name', 'description')
        }),
        ('Timeline', {
            'fields': ('deadline', 'created_at', 'updated_at', 'completed_at')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Achievement)
admin.site.register(Goal, GoalAdmin)


# ============================================================================
# COURSE ADMIN
# ============================================================================

class CourseResourceInline(admin.TabularInline):
    """Inline editor for course resources"""
    model = CourseResource
    extra = 0
    fields = ('title', 'resource_type', 'platform', 'quality_rating', 'is_free', 'is_official')
    readonly_fields = ('created_at',)


class CourseAdmin(admin.ModelAdmin):
    """Admin interface for courses"""
    list_display = ('name', 'user', 'category', 'level', 'status', 'duration_hours', 'resource_count', 'created_at')
    list_filter = ('status', 'level', 'category', 'created_at')
    search_fields = ('name', 'user__username', 'user__email', 'category')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'published_at', 'resource_count', 'total_resource_hours')
    inlines = (CourseResourceInline,)
    
    fieldsets = (
        ('Course Information', {
            'fields': ('user', 'name', 'description', 'category')
        }),
        ('Level & Status', {
            'fields': ('level', 'status')
        }),
        ('Content Details', {
            'fields': ('duration_hours', 'prerequisites', 'learning_outcomes')
        }),
        ('Statistics', {
            'fields': ('resource_count', 'total_resource_hours'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )


class CourseResourceAdmin(admin.ModelAdmin):
    """Admin interface for course resources"""
    list_display = ('title', 'course', 'resource_type', 'platform', 'quality_rating', 'is_free', 'is_official', 'is_trending', 'created_at')
    list_filter = ('resource_type', 'quality_rating', 'is_free', 'is_official', 'is_trending', 'difficulty_level', 'created_at')
    search_fields = ('title', 'description', 'course__name', 'platform')
    ordering = ('-quality_rating', '-is_official', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Resource Information', {
            'fields': ('course', 'title', 'description')
        }),
        ('Type & Classification', {
            'fields': ('resource_type', 'difficulty_level')
        }),
        ('Source', {
            'fields': ('url', 'platform', 'duration_hours')
        }),
        ('Quality & Curation', {
            'fields': ('quality_rating', 'is_free', 'is_official', 'is_trending')
        }),
        ('Metadata', {
            'fields': ('added_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class CourseEnrollmentAdmin(admin.ModelAdmin):
    """Admin interface for course enrollments"""
    list_display = ('user', 'course', 'status', 'progress_percentage', 'resources_completed', 'enrolled_at')
    list_filter = ('status', 'enrolled_at', 'started_at', 'completed_at')
    search_fields = ('user__username', 'user__email', 'course__name')
    ordering = ('-enrolled_at',)
    readonly_fields = ('enrolled_at', 'started_at', 'completed_at')
    
    fieldsets = (
        ('Enrollment', {
            'fields': ('user', 'course', 'status')
        }),
        ('Progress', {
            'fields': ('progress_percentage', 'resources_completed')
        }),
        ('Timestamps', {
            'fields': ('enrolled_at', 'started_at', 'completed_at')
        }),
    )


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseResource, CourseResourceAdmin)
admin.site.register(CourseEnrollment, CourseEnrollmentAdmin)
