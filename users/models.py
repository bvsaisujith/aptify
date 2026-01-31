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
