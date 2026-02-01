import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

def generate_8_digit_code():
    """Generates a unique 8-digit numeric string for the Public ID."""
    return get_random_string(8, allowed_chars='0123456789')

class User(AbstractUser):
    """
    IDENTITY LAYER: Handles authentication and DPDP compliance.
    """
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin'),
    )

    # Use standard BigAutoField internally for DB performance, 
    # but use the 8-digit code as the public-facing unique identifier.
    user_code = models.CharField(
        max_length=8, 
        unique=True, 
        default=generate_8_digit_code,
        editable=False,
        db_index=True
    )
    email = models.EmailField(_('email address'), unique=True, null=False, blank=False) # Mandatory
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES,
        default='candidate'
    )
    
    # DPDP Compliance: Tracking when the user gave explicit consent.
    consent_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['email', 'user_code']),
        ]

    def __str__(self):
        return f"{self.username} ({self.user_code})"

class Profile(models.Model):
    """
    PROFILE LAYER: Stores mandatory personal details (PII).
    Separating this allows for high-speed 'Identity-only' lookups .
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, null=False, blank=False) # Mandatory
    dob = models.DateField(null=True, blank=True) # Make optional initially to allow registration steps
    
    # Use ImageField (storing only the URL/Path in DB) for performance .
    profile_photo = models.ImageField(upload_to='profiles/%Y/%m/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.user_code})"

class Achievement(models.Model):
    """
    ACHIEVEMENT LAYER: Normalized for Skill Intelligence and Blockchain.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255)
    issued_by = models.CharField(max_length=255)
    date_earned = models.DateField()
    
    # 2026 Standards: Link to a blockchain-verified record .
    blockchain_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['blockchain_hash']),
        ]

    def __str__(self):
        return f"{self.title} - {self.profile.full_name}"


class Goal(models.Model):
    """
    GOALS LAYER: User-defined learning and achievement goals.
    """
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    name = models.CharField(max_length=255, help_text="Goal title or description")
    description = models.TextField(blank=True, help_text="Detailed description of the goal")
    
    # Deadline can be flexible: specific date, month, or year
    deadline = models.DateField(help_text="Target deadline for this goal")
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['deadline', '-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['deadline']),
        ]

    def __str__(self):
        return f"{self.name} - {self.user.username} ({self.status})"
    
    @property
    def is_overdue(self):
        """Check if goal deadline has passed"""
        from django.utils import timezone
        return self.deadline < timezone.now().date() and self.status != 'completed'
    
    @property
    def days_remaining(self):
        """Calculate days until deadline"""
        from django.utils import timezone
        delta = self.deadline - timezone.now().date()
        return delta.days if delta.days > 0 else 0


class Course(models.Model):
    """
    COURSES LAYER: Learning courses with aggregated resources.
    """
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created')
    name = models.CharField(max_length=255, help_text="Course name")
    description = models.TextField(help_text="Detailed course description")
    category = models.CharField(max_length=100, help_text="Course category (e.g., AI, Python, Web Development)")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    
    # Course metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    duration_hours = models.IntegerField(help_text="Estimated duration in hours", null=True, blank=True)
    prerequisites = models.TextField(blank=True, help_text="Any prerequisites or recommended prior knowledge")
    
    # Learning outcomes
    learning_outcomes = models.TextField(blank=True, help_text="What students will learn (comma-separated)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['category', 'level']),
        ]

    def __str__(self):
        return f"{self.name} ({self.level})"
    
    @property
    def resource_count(self):
        return self.resources.count()
    
    @property
    def total_resource_hours(self):
        """Calculate total hours from all resources"""
        return sum(r.duration_hours for r in self.resources.all() if r.duration_hours) or 0


class CourseResource(models.Model):
    """
    COURSE RESOURCES: Aggregated learning resources (no video links, curated alternatives).
    """
    RESOURCE_TYPE_CHOICES = (
        ('documentation', 'Documentation'),
        ('tutorial', 'Tutorial'),
        ('article', 'Article'),
        ('interactive', 'Interactive Learning'),
        ('book', 'Book'),
        ('course', 'Online Course'),
        ('repository', 'GitHub Repository'),
        ('podcast', 'Podcast'),
        ('tool', 'Tool/Framework'),
        ('practice', 'Practice Problems'),
    )
    
    QUALITY_CHOICES = (
        ('excellent', '⭐⭐⭐⭐⭐ Excellent'),
        ('very_good', '⭐⭐⭐⭐ Very Good'),
        ('good', '⭐⭐⭐ Good'),
        ('fair', '⭐⭐ Fair'),
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255, help_text="Resource title")
    description = models.TextField(help_text="What this resource covers")
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE_CHOICES)
    
    # Resource details
    url = models.URLField(help_text="URL to the resource")
    platform = models.CharField(max_length=100, help_text="Platform (e.g., freeCodeCamp, MDN, Stack Overflow)")
    
    # Metadata
    duration_hours = models.IntegerField(null=True, blank=True, help_text="Duration in hours (if applicable)")
    quality_rating = models.CharField(
        max_length=20, 
        choices=QUALITY_CHOICES, 
        default='good',
        help_text="Quality rating (curated assessment)"
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default='beginner'
    )
    
    # Relevance
    is_free = models.BooleanField(default=True, help_text="Is this resource free?")
    is_official = models.BooleanField(default=False, help_text="Is this official documentation/resource?")
    is_trending = models.BooleanField(default=False, help_text="Is this a trending/popular resource?")
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resources_added')
    
    class Meta:
        ordering = ['-quality_rating', '-is_official', '-created_at']
        indexes = [
            models.Index(fields=['course', 'resource_type']),
            models.Index(fields=['is_free', 'is_trending']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"
    
    @property
    def get_star_rating(self):
        """Return numeric star rating"""
        ratings = {
            'excellent': 5,
            'very_good': 4,
            'good': 3,
            'fair': 2,
        }
        return ratings.get(self.quality_rating, 3)


class CourseEnrollment(models.Model):
    """
    COURSE ENROLLMENT: Track user progress through courses.
    """
    STATUS_CHOICES = (
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    
    # Progress tracking
    progress_percentage = models.IntegerField(default=0, help_text="Percentage of course completed")
    resources_completed = models.IntegerField(default=0)
    
    # Timestamps
    enrolled_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'course')
        indexes = [
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

