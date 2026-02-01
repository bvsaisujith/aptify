# Courses System - Quick Start Guide

## Getting Started

### 1. Accessing Courses
From the dashboard, click **📚 Explore Courses** or navigate to:
```
http://localhost:8000/courses/
```

### 2. Creating Your First Course

#### Step 1: Click "➕ Create New Course"
- Navigate to `/courses/create/`

#### Step 2: Fill in Course Information
```
Course Name:     "Python for Beginners"
Description:     "Learn Python fundamentals with hands-on exercises"
Category:        "Python"
Level:           "Beginner"
Duration:        "40 hours"
```

#### Step 3: Add Learning Details
```
Prerequisites:   "Basic computer knowledge"
Learning Outcomes: "Variables, loops, functions, data structures"
```

#### Step 4: Save Course
- Course created as **Draft** (not published yet)
- Auto-redirects to course detail page

### 3. Adding Resources

#### Step 1: Click "➕ Add Resource"
- On course detail page

#### Step 2: Add Resource Information
```
Resource Title:    "Python Tutorial - W3Schools"
Description:       "Complete interactive Python tutorial"
Resource Type:     "Tutorial"
```

#### Step 3: Provide Source Link
```
URL:              https://www.w3schools.com/python/
Platform:         "W3Schools"
Duration:         "20 hours"
```

#### Step 4: Set Quality Metrics
```
Quality Rating:   ⭐⭐⭐⭐ (Very Good)
Free Resource:    ✓ Yes
Official:         ✗ No
Trending:         ✓ Yes
Difficulty:       "Beginner"
```

#### Step 5: Save Resource
- Resource added and sorted by quality
- Appears in course detail page

### 4. Browsing Resources

#### View All Resources
1. Go to course detail page
2. See all resources sorted by quality (best first)
3. Resources show:
   - Title and description
   - Type (Tutorial, Documentation, etc.)
   - Platform (W3Schools, MDN, etc.)
   - Quality rating (2-5 stars)
   - Flags (Free ✓, Official ✓, Trending 🔥)

#### Filter Resources by Type
```
Quick-access buttons:
- All Resources
- Documentation (count)
- Tutorial (count)
- Articles (count)
- Interactive (count)
... (10 types total)
```

#### Access Resources
1. Click "🔗 View" button
2. Opens resource in new tab
3. Links to best curated alternative

### 5. Managing Courses

#### View All Courses
```
GET /courses/
```
Shows:
- Course grid (12 per page)
- Resource statistics
- Duration information
- Quick edit/delete actions

#### Filter Courses
```
By Category:  "AI", "Python", "Web Development"
By Level:     "Beginner", "Intermediate", "Advanced", "Expert"
Sort By:      "Newest First", "Name (A-Z)", "Level", "Recently Updated"
```

#### Edit Course
```
/courses/<id>/edit/
```
Update any course information

#### Delete Course
```
/courses/<id>/delete/
```
Safe deletion with confirmation (cascades to resources)

### 6. Resource Types

Choose from 10 resource types:

| Type | Example | Use Case |
|------|---------|----------|
| 📚 **Documentation** | API Reference | Official guides |
| 📖 **Tutorial** | Step-by-step guide | Learning basics |
| 📄 **Article** | Blog post | Deep dives |
| 🎮 **Interactive** | Code sandbox | Hands-on practice |
| 📕 **Book** | O'Reilly | Comprehensive learning |
| 🎓 **Online Course** | Coursera | Structured learning |
| 🔗 **Repository** | GitHub | Code examples |
| 🎙️ **Podcast** | Developer podcast | Audio learning |
| 🛠️ **Tool/Framework** | VS Code | Development tools |
| ✏️ **Practice** | LeetCode | Coding challenges |

### 7. Quality Rating System

```
⭐⭐⭐⭐⭐ Excellent (5 stars)
   - Official, well-maintained, highly recommended
   
⭐⭐⭐⭐ Very Good (4 stars)
   - High quality, regularly updated
   
⭐⭐⭐ Good (3 stars)
   - Solid content, minor issues
   
⭐⭐ Fair (2 stars)
   - Acceptable but has limitations
```

### 8. Using Flags

```
💰 Free Resource
   - No payment required
   - Accessible to everyone
   
✅ Official Resource
   - From original creator/organization
   - Most trustworthy source
   
🔥 Trending
   - Currently popular
   - Recently gaining attention
```

### 9. Common Workflows

#### Workflow 1: Create Complete Learning Path
```
1. Create Course: "Machine Learning Fundamentals"
2. Add Resource: "ML Documentation" (Official)
3. Add Resource: "ML Tutorial" (Free, Trending)
4. Add Resource: "ML Article" (Deep dive)
5. Add Resource: "Practice Problems" (Interactive)
6. Add Resource: "ML Podcast" (Supplementary)
```

#### Workflow 2: Find Best Resource for Topic
```
1. Search course by topic
2. View course detail
3. Resources pre-sorted by quality
4. Scan for Free + Official flags
5. Click relevant resource link
6. Access best curated alternative
```

#### Workflow 3: Manage Multiple Courses
```
1. View all courses (/courses/)
2. Filter by category/level
3. See at-a-glance stats (resources, hours)
4. Quick edit/delete from grid
5. Update course information
6. Add/remove resources
```

### 10. Tips & Best Practices

#### Adding Resources
- ✓ Mix resource types for diverse learning
- ✓ Prioritize Official sources
- ✓ Mark Free resources for accessibility
- ✓ Update quality ratings honestly
- ✓ Include diverse platforms
- ✓ Add fresh Trending resources
- ✓ Verify URLs work correctly

#### Creating Courses
- ✓ Be specific about prerequisites
- ✓ Clear, measurable learning outcomes
- ✓ Realistic duration estimates
- ✓ Organized by difficulty progression
- ✓ Mix theory and practice resources
- ✓ Include official documentation
- ✓ Add practical, hands-on projects

#### Curating Resources
- ✓ Test resources before adding
- ✓ Verify links are current
- ✓ Check resource quality regularly
- ✓ Update ratings based on feedback
- ✓ Remove outdated content
- ✓ Add alternatives for better coverage
- ✓ Document why resource is valuable

### 11. Admin Access

#### Access Django Admin
```
http://localhost:8000/aptify-admin/
```

#### Manage Courses
- View all courses
- Edit course details
- Add/edit/delete resources inline
- Track enrollment progress
- Monitor resource quality

#### Filter Resources
- By platform
- By quality rating
- By resource type
- By free/official/trending status

### 12. Navigation

```
Dashboard Links:
├─ Overview
├─ Courses ← NEW
├─ Goals
├─ Assignments
├─ Analysis
└─ Settings

Courses Page Links:
├─ Create New Course
├─ View Course Details
├─ Edit Course
├─ Delete Course
├─ Add Resources
└─ Filter & Sort
```

### 13. Troubleshooting

#### Issue: Can't see courses
- **Solution**: Make sure you're logged in
- **Check**: User authentication status

#### Issue: Resource link not working
- **Solution**: Edit resource and verify URL
- **Action**: Update or delete invalid resource

#### Issue: Course not showing resources
- **Solution**: Navigate to course detail page
- **Action**: Click "Add Resource" to add content

#### Issue: Filter not working
- **Solution**: Refresh the page
- **Action**: Reapply filters

### 14. Advanced Features

#### Resource Filtering (JavaScript-based)
```javascript
// Filter resources by type in real-time
// No page reload required
// Multiple types can be selected
// "All Resources" shows everything
```

#### Pagination
```
12 courses per page
← Previous | Page X of Y | Next →
```

#### Search
```
Admin interface: Search by
- Course name
- Category
- User who created it
- Resource title
- Platform name
```

### 15. Performance Notes

- Course list paginated (12 per page)
- Resources indexed for fast queries
- Quality-based sorting optimized
- Admin searches use database indexes
- Responsive design loads quickly

---

## That's it! 🎉

You now have a complete course management system with:
- ✅ Multiple resource types
- ✅ Quality-based curation
- ✅ No direct video links (strategic redirection)
- ✅ Official resource verification
- ✅ Free resource prioritization
- ✅ Trending indicator
- ✅ Professional dark UI
- ✅ Full admin control

**Ready to start building your learning paths!** 📚
