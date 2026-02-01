# AptiFy Courses System

## Overview

The AptiFy Courses system is a comprehensive learning management platform that allows users to create, organize, and share personalized learning paths with aggregated, curated resources. Instead of directing users to video links, our system redirects to the best available resources across multiple platforms.

## Features

### 1. Course Management

**Create Courses**
- Course name and detailed description
- Category and difficulty level (Beginner → Intermediate → Advanced → Expert)
- Estimated duration in hours
- Prerequisites specification
- Learning outcomes definition

**Edit & Delete Courses**
- Modify course details at any time
- Track resource count and total hours
- Archive or publish courses

### 2. Resource Aggregation

**No Direct Video Links** - Instead, we aggregate resources by type:
- 📚 Documentation
- 📖 Tutorials  
- 📄 Articles
- 🎮 Interactive Learning
- 📕 Books
- 🎓 Online Courses
- 🔗 GitHub Repositories
- 🎙️ Podcasts
- 🛠️ Tools/Frameworks
- ✏️ Practice Problems

**Resource Quality System**
- ⭐⭐⭐⭐⭐ Excellent (5 stars)
- ⭐⭐⭐⭐ Very Good (4 stars)
- ⭐⭐⭐ Good (3 stars)
- ⭐⭐ Fair (2 stars)

**Resource Metadata**
- Platform tracking (freeCodeCamp, MDN, Stack Overflow, etc.)
- Free/Paid flag
- Official/Verified status
- Trending indicator
- Difficulty level
- Duration in hours (when applicable)

### 3. User Features

**Browse Courses**
- Filter by category, level, or status
- Sort by newest, alphabetical, or last updated
- View resource statistics per course
- Pagination (12 courses per page)

**Enroll in Courses**
- Track enrollment status (Enrolled/In Progress/Completed/Abandoned)
- Monitor progress percentage
- Track resources completed

**Curated Resource Discovery**
- View all resources with quality ratings
- Filter resources by type
- Identify free resources
- Discover official documentation
- Find trending resources
- Direct links to best alternatives

## URL Routes

```
/courses/                    - List all courses
/courses/create/             - Create new course
/courses/<id>/               - View course details
/courses/<id>/edit/          - Edit course
/courses/<id>/delete/        - Delete course
/courses/<id>/resources/add/ - Add resource to course
/resources/<id>/edit/        - Edit resource
/resources/<id>/delete/      - Delete resource
```

## Database Models

### Course Model
```python
- user (ForeignKey to User)
- name, description
- category, level
- status (draft/published/archived)
- duration_hours
- prerequisites, learning_outcomes
- created_at, updated_at, published_at
```

### CourseResource Model
```python
- course (ForeignKey to Course)
- title, description
- resource_type (10 types available)
- url, platform
- duration_hours
- quality_rating (2-5 stars)
- difficulty_level
- is_free, is_official, is_trending (flags)
- created_at, updated_at
- added_by (ForeignKey to User)
```

### CourseEnrollment Model
```python
- user, course (unique together)
- status (enrolled/in_progress/completed/abandoned)
- progress_percentage (0-100)
- resources_completed (count)
- enrolled_at, started_at, completed_at
```

## Admin Interface

Full admin support with:
- Course inline resource editor
- Resource filtering and search
- Enrollment tracking
- Quality rating visualization
- Status and platform filtering

## Views

All views require authentication (LoginRequiredMixin)

**CourseListView**
- Lists user's courses
- Filtering by category and level
- Sorting options
- Pagination

**CourseCreateView / CourseUpdateView**
- Form validation
- Timestamps management
- Success messages

**CourseDetailView**
- Full course information
- All resources grouped by type
- Resource filtering by type
- Quality-based sorting

**CourseResourceCreateView / UpdateView**
- Add resources to courses
- Update resource metadata
- Quality rating selection

**CourseResourceDeleteView**
- Safe deletion with confirmation
- Cascade handling

## Forms

### CourseForm
Fields: name, description, category, level, duration_hours, prerequisites, learning_outcomes

### CourseResourceForm
Fields: title, description, resource_type, url, platform, duration_hours, quality_rating, difficulty_level, is_free, is_official, is_trending

### CourseFilterForm
Filters: category, level, sort options

## Templates

**course_list.html**
- Course grid with statistics
- Filter and sort controls
- Empty state messaging
- Pagination

**course_form.html**
- Create/Edit form
- Field validation
- Course information sidebar
- Quick actions

**course_detail.html**
- Course overview with badges
- Learning outcomes list
- Prerequisites section
- Resource table with quality ratings
- Resource type filtering
- Flag indicators
- Direct resource links

**course_resource_form.html**
- Resource type selection
- Quality rating selector
- Free/Official/Trending flags
- Tips for adding resources
- Form validation

**course_confirm_delete.html & course_resource_confirm_delete.html**
- Safety confirmation dialogs
- Clear warning messages
- Cancel/Confirm buttons

## Styling

All pages follow the Intelligence Dark theme:
- Primary: #8b5cf6 (Vivid Violet)
- Accent: #22d3ee (Cyan Neon)
- Background: #0f172a (Midnight)
- Text: #f8fafc (Pure White)
- Responsive design for mobile/tablet/desktop

## Key Differentiators

1. **No Video Links**: Redirect to curated alternatives instead
2. **Quality Rating System**: Guide users to best resources
3. **Platform Tracking**: Know where content comes from
4. **Resource Type Diversity**: Support all learning modalities
5. **Community Curation**: Track who added resources
6. **Trending Indicator**: Highlight popular resources
7. **Free Resource Priority**: Filter by accessibility
8. **Official Verification**: Mark official documentation

## Usage Examples

### Creating a Course
1. Navigate to Courses → Create New Course
2. Enter course name, description, category
3. Select difficulty level and estimated hours
4. Add prerequisites and learning outcomes
5. Save course (starts as draft)
6. Add resources from course detail page

### Adding Resources
1. Open course detail
2. Click "Add Resource"
3. Select resource type (Documentation, Tutorial, etc.)
4. Enter resource title, description, URL
5. Choose quality rating
6. Mark flags (Free, Official, Trending)
7. Save resource

### Discovering Best Resources
1. Browse courses
2. View course detail
3. Resources sorted by quality rating and official status
4. Filter by resource type
5. Click resource link to access best alternative

## Future Enhancements

- Resource import from APIs (freeCodeCamp, MDN, etc.)
- Community contributions with moderation
- Course recommendations based on progress
- Resource comments and ratings by users
- Completion certificates
- Learning analytics and recommendations
- Collaborative course creation
- Resource caching and offline access

## Implementation Notes

- All models include timestamps for tracking
- Unique constraints prevent duplicate enrollments
- Indexes on frequently queried fields
- Soft delete support for published courses
- Quality metadata automatically maintains sort order
- User tracking for attribution and community features
