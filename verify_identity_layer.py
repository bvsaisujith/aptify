import os
import django
import sys

# Setup Django environment
sys.path.append('/home/bvdanger/AptiFy')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aptify.settings')
django.setup()

from users.models import User, Profile, Achievement
from django.db import transaction

def verify_identity_layer():
    print("Verifying Sovereign Identity Identity Layer...")
    
    # Clean up previous test data
    User.objects.filter(email='testcandidate@example.com').delete()

    # 1. Create a User
    print("1. Creating User 'testuser'...")
    user = User.objects.create_user(
        username='testuser', 
        email='testcandidate@example.com', 
        password='TestPassword123!'
    )
    
    # 2. Verify 8-digit Code
    print(f"   User Code: {user.user_code}")
    assert len(user.user_code) == 8, "User code must be 8 digits"
    assert user.user_code.isdigit(), "User code must be numeric"
    print("   [PASS] 8-digit User Code generated.")

    # 3. Verify Profile Auto-Creation (Signal)
    print("2. Verifying Profile Auto-Creation...")
    try:
        profile = user.profile
        print(f"   Profile found: {profile}")
        assert profile.user == user, "Profile user mismatch"
        assert profile.full_name == user.username, "Profile full_name default mismatch"
        print("   [PASS] Profile automatically created via signal.")
    except Profile.DoesNotExist:
        print("   [FAIL] Profile NOT created!")
        exit(1)

    # 4. Verify Authorization/Role default
    print(f"   Role: {user.role}")
    assert user.role == 'candidate', "Default role should be 'candidate'"
    print("   [PASS] Default role is Correct.")

    # 5. Verify Achievement Creation
    print("3. Creating Achievement...")
    achievement = Achievement.objects.create(
        profile=profile,
        title="Django Certified Developer",
        issued_by="Django Software Foundation",
        date_earned="2026-01-01",
        blockchain_hash="0x123abc456def"
    )
    print(f"   Achievement: {achievement}")
    assert achievement.profile == profile
    print("   [PASS] Achievement created and linked to Profile.")

    print("\nSUCCESS: Sovereign Identity Architecture Verified!")

if __name__ == "__main__":
    try:
        verify_identity_layer()
    except Exception as e:
        print(f"\n[ERROR] Verification Failed: {e}")
        exit(1)
