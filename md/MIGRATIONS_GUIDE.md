# Database Migrations & Setup Guide

## Migration History

### Migration 0001: Initial User Setup
**File:** `users/migrations/0001_initial.py`
**Created:** Initial project setup
**Models:** User, Profile, Achievement

### Migration 0002: Goals System
**File:** `users/migrations/0002_goal.py`
**Created:** Goal model for learning objectives
**Models:** Goal

### Migration 0003: Courses System ✓ (THIS SESSION)
**File:** `users/migrations/0003_course_courseenrollment_courseresource_and_more.py`
**Created:** Complete courses system
**Models:** 
- Course
- CourseResource
- CourseEnrollment

**Status:** ✅ Successfully Applied

---

## Applying Migrations

### Step 1: Verify Environment
```bash
cd /home/bvdanger/AptiFy
source .venv/bin/activate
```

### Step 2: Create Migrations (if needed)
```bash
python manage.py makemigrations users
```
**Output:** `No changes detected in app 'users'` (already migrated)

### Step 3: Apply Migrations
```bash
python manage.py migrate users
```
**Output:**
```
Operations to perform:
  Apply all migrations: users
Running migrations:
  Applying users.0003_course_courseenrollment_courseresource_and_more... OK
```

### Step 4: Verify
```bash
python manage.py check
```
**Output:** System check passed (warnings about Allauth are normal)

---

## Database Schema

### Course Table
```sql
CREATE TABLE users_course (
  id                INTEGER PRIMARY KEY,
  user_id           INTEGER NOT NULL,
  name              VARCHAR(255),
  description       TEXT,
  category          VARCHAR(100),
  level             VARCHAR(20),
  status            VARCHAR(20),
  duration_hours    INTEGER,
  prerequisites     TEXT,
  learning_outcomes TEXT,
  created_at        DATETIME,
  updated_at        DATETIME,
  published_at      DATETIME,
  
  FOREIGN KEY (user_id) REFERENCES users_user(id),
  INDEX (user_id, status),
  INDEX (category, level)
);
```

### CourseResource Table
```sql
CREATE TABLE users_courseresource (
  id                  INTEGER PRIMARY KEY,
  course_id           INTEGER NOT NULL,
  added_by_id         INTEGER,
  title               VARCHAR(255),
  description         TEXT,
  resource_type       VARCHAR(50),
  url                 VARCHAR(200),
  platform            VARCHAR(100),
  duration_hours      INTEGER,
  quality_rating      VARCHAR(20),
  difficulty_level    VARCHAR(20),
  is_free             BOOLEAN,
  is_official         BOOLEAN,
  is_trending         BOOLEAN,
  created_at          DATETIME,
  updated_at          DATETIME,
  
  FOREIGN KEY (course_id) REFERENCES users_course(id),
  FOREIGN KEY (added_by_id) REFERENCES users_user(id),
  INDEX (course_id, resource_type),
  INDEX (is_free, is_trending)
);
```

### CourseEnrollment Table
```sql
CREATE TABLE users_courseenrollment (
  id                  INTEGER PRIMARY KEY,
  user_id             INTEGER NOT NULL,
  course_id           INTEGER NOT NULL,
  status              VARCHAR(20),
  progress_percentage INTEGER,
  resources_completed INTEGER,
  enrolled_at         DATETIME,
  started_at          DATETIME,
  completed_at        DATETIME,
  
  FOREIGN KEY (user_id) REFERENCES users_user(id),
  FOREIGN KEY (course_id) REFERENCES users_course(id),
  UNIQUE (user_id, course_id),
  INDEX (user_id, status)
);
```

---

## Data Population

### Creating Sample Course
```python
# Django Shell
python manage.py shell

from users.models import Course, CourseResource
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()

course = Course.objects.create(
    user=user,
    name="Python for Beginners",
    description="Learn Python fundamentals",
    category="Programming",
    level="beginner",
    status="published",
    duration_hours=40,
    prerequisites="Basic computer knowledge",
    learning_outcomes="Variables, loops, functions, data structures"
)

resource = CourseResource.objects.create(
    course=course,
    title="Python Tutorial",
    description="Interactive Python tutorial",
    resource_type="tutorial",
    url="https://www.w3schools.com/python/",
    platform="W3Schools",
    duration_hours=20,
    quality_rating="very_good",
    is_free=True,
    is_official=False,
    is_trending=True,
    added_by=user
)

print(f"Created course: {course.name}")
print(f"Added resource: {resource.title}")
```

---

## Database Queries

### Find All Courses by User
```python
from users.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='john')
courses = Course.objects.filter(user=user)
```

### Find Top-Rated Resources
```python
from users.models import CourseResource

resources = CourseResource.objects.filter(
    quality_rating__in=['excellent', 'very_good']
).order_by('-quality_rating', '-is_official')
```

### Find Free Resources
```python
free_resources = CourseResource.objects.filter(
    is_free=True
).order_by('-is_official', '-created_at')
```

### Find Official Resources
```python
official_resources = CourseResource.objects.filter(
    is_official=True
)
```

### Find Trending Resources
```python
trending = CourseResource.objects.filter(
    is_trending=True
)
```

### Count Resources per Course
```python
from django.db.models import Count

courses_with_counts = Course.objects.annotate(
    resource_count=Count('resources')
)

for course in courses_with_counts:
    print(f"{course.name}: {course.resource_count} resources")
```

### Find User Enrollments
```python
from users.models import CourseEnrollment

enrollments = CourseEnrollment.objects.filter(
    user=user,
    status='in_progress'
)
```

### Calculate Total Learning Hours
```python
from django.db.models import Sum

total_hours = CourseResource.objects.filter(
    duration_hours__isnull=False
).aggregate(total=Sum('duration_hours'))

print(f"Total learning hours: {total_hours['total']}")
```

---

## Backup & Restore

### Backup Database
```bash
# SQLite backup
cp db.sqlite3 db.sqlite3.backup

# Or create dated backup
cp db.sqlite3 db.sqlite3.$(date +%Y%m%d_%H%M%S).backup
```

### Restore Database
```bash
# Restore from backup
cp db.sqlite3.backup db.sqlite3
```

### Export Data
```bash
# JSON export
python manage.py dumpdata users > courses_data.json

# Specific model
python manage.py dumpdata users.Course > courses_only.json
```

### Import Data
```bash
# Restore from JSON
python manage.py loaddata courses_data.json
```

---

## Clearing Data

### Reset Database
```bash
# Delete and recreate
python manage.py migrate users --plan
python manage.py migrate users zero  # Revert all migrations
python manage.py migrate users       # Reapply all migrations
```

### Clear Specific Model
```bash
python manage.py shell

from users.models import CourseResource
CourseResource.objects.all().delete()
```

---

## Performance Optimization

### Query Optimization
```python
# BAD: N+1 queries
courses = Course.objects.all()
for course in courses:
    print(course.user.username)  # Extra query per course

# GOOD: Join with select_related
courses = Course.objects.select_related('user')
for course in courses:
    print(course.user.username)  # No extra queries
```

### Prefetch Related Objects
```python
# For many-to-many relationships
courses = Course.objects.prefetch_related('resources')

for course in courses:
    for resource in course.resources.all():
        print(resource.title)  # Efficient querying
```

### Adding Indexes
```python
# Already added in model Meta:
class Meta:
    indexes = [
        models.Index(fields=['user', 'status']),
        models.Index(fields=['category', 'level']),
    ]
```

### Pagination
```python
# Automatic pagination reduces memory usage
from django.core.paginator import Paginator

courses = Course.objects.all()
paginator = Paginator(courses, 12)

page = paginator.page(1)
print(page.object_list)  # 12 items only
```

---

## Monitoring

### Check Database Size
```bash
# SQLite
ls -lh db.sqlite3

# Database info
sqlite3 db.sqlite3 ".tables"
sqlite3 db.sqlite3 "SELECT name FROM sqlite_master WHERE type='table';"
```

### Count Records
```bash
python manage.py shell

from users.models import Course, CourseResource, CourseEnrollment

print(f"Courses: {Course.objects.count()}")
print(f"Resources: {CourseResource.objects.count()}")
print(f"Enrollments: {CourseEnrollment.objects.count()}")
```

### Find Database Bottlenecks
```bash
# Enable query logging
python manage.py shell

from django.db import connection

# Run queries then check
print(len(connection.queries))  # Number of queries
for query in connection.queries:
    print(query['sql'])  # SQL statement
```

---

## Troubleshooting

### Migration Conflicts
**Problem:** `Conflicting migrations detected`
**Solution:**
```bash
python manage.py migrate --fake-initial
```

### Database Locked
**Problem:** `database is locked`
**Solution:**
```bash
# Kill Django processes
pkill -f runserver

# Restart fresh
python manage.py runserver
```

### Migration Not Applied
**Problem:** Migration file exists but not applied
**Solution:**
```bash
# Check status
python manage.py showmigrations users

# Force apply
python manage.py migrate users --run-syncdb
```

### Syntax Errors in Migration
**Problem:** Migration fails to apply
**Solution:**
```bash
# View migration file
cat users/migrations/000X_*.py

# Check for errors
python manage.py check

# Rollback to previous
python manage.py migrate users [previous_number]
```

---

## Deployment Checklist

- [ ] Backup production database
- [ ] Test migrations on staging
- [ ] Create migration if models changed
- [ ] Run `python manage.py check`
- [ ] Apply migrations: `python manage.py migrate`
- [ ] Verify admin interface
- [ ] Test course creation
- [ ] Test resource addition
- [ ] Monitor for errors
- [ ] Verify data integrity

---

## Migration Commands Reference

```bash
# Make migrations
python manage.py makemigrations users

# Show migration plan
python manage.py migrate users --plan

# Apply migrations
python manage.py migrate users

# Rollback last migration
python manage.py migrate users [migration_before]

# Show migration history
python manage.py showmigrations users

# SQL preview
python manage.py sqlmigrate users 0003

# Fake migration (mark as applied without running)
python manage.py migrate users --fake

# Zero out all migrations
python manage.py migrate users zero
```

---

## Database Statistics

**Current Schema:**
- Tables: 10+
- Indexes: 10+
- Models: 7 (User, Profile, Achievement, Goal, Course, CourseResource, CourseEnrollment)
- Migrations: 3

**Estimated Data Volume (per 1000 users):**
- Courses: ~5,000
- Resources: ~25,000
- Enrollments: ~10,000
- Database size: ~50MB

---

## Maintenance Schedule

### Daily
- Monitor error logs
- Check database size

### Weekly
- Backup database
- Verify migrations applied

### Monthly
- Analyze query performance
- Review database indexes
- Archive old data (if applicable)

---

## Security Considerations

1. **Database Access**
   - SQLite file permissions: 600
   - Production: Use PostgreSQL with SSL
   - No sensitive data in logs

2. **Data Protection**
   - Backups encrypted
   - Access restricted
   - Regular testing of restores

3. **Migration Safety**
   - Test on staging first
   - Backup before applying
   - Document changes
   - Version control migrations

---

## Documentation

For more information, see:
- `COURSES_SYSTEM.md` - Feature documentation
- `COURSES_IMPLEMENTATION.md` - Implementation details
- `ARCHITECTURE.md` - Design decisions
- `COURSES_QUICKSTART.md` - User guide
