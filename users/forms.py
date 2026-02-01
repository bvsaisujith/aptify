from django import forms
from users.models import Goal, Course, CourseResource


class GoalForm(forms.ModelForm):
    """Form for creating and editing user goals"""
    
    class Meta:
        model = Goal
        fields = ['name', 'description', 'deadline', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter goal name',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your goal (optional)',
                'rows': 4
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Goal Name',
            'description': 'Description',
            'deadline': 'Target Deadline',
            'status': 'Status',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set minimum date to today
        from django.utils import timezone
        self.fields['deadline'].widget.attrs['min'] = timezone.now().date().isoformat()


class GoalFilterForm(forms.Form):
    """Form for filtering goals"""
    
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    SORT_CHOICES = [
        ('deadline', 'Deadline (Ascending)'),
        ('-deadline', 'Deadline (Descending)'),
        ('-created_at', 'Newest First'),
        ('created_at', 'Oldest First'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='deadline',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class CourseForm(forms.ModelForm):
    """Form for creating and editing courses"""
    
    class Meta:
        model = Course
        fields = ['name', 'description', 'category', 'level', 'duration_hours', 'prerequisites', 'learning_outcomes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course name',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the course content',
                'rows': 5
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., AI, Python, Web Development'
            }),
            'level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estimated hours to complete',
                'type': 'number'
            }),
            'prerequisites': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any required prior knowledge',
                'rows': 3
            }),
            'learning_outcomes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'What students will learn (comma-separated)',
                'rows': 3
            }),
        }
        labels = {
            'name': 'Course Name',
            'description': 'Description',
            'category': 'Category',
            'level': 'Difficulty Level',
            'duration_hours': 'Estimated Duration (hours)',
            'prerequisites': 'Prerequisites',
            'learning_outcomes': 'Learning Outcomes',
        }


class CourseResourceForm(forms.ModelForm):
    """Form for adding course resources"""
    
    class Meta:
        model = CourseResource
        fields = ['title', 'description', 'resource_type', 'url', 'platform', 'duration_hours', 
                  'quality_rating', 'difficulty_level', 'is_free', 'is_official', 'is_trending']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resource title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'What does this resource cover?',
                'rows': 3
            }),
            'resource_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/resource'
            }),
            'platform': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., freeCodeCamp, MDN, GitHub'
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in hours (if applicable)',
                'type': 'number'
            }),
            'quality_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'difficulty_level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_free': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_official': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_trending': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'title': 'Resource Title',
            'description': 'Description',
            'resource_type': 'Resource Type',
            'url': 'Resource URL',
            'platform': 'Platform',
            'duration_hours': 'Duration (hours)',
            'quality_rating': 'Quality Rating',
            'difficulty_level': 'Difficulty Level',
            'is_free': 'Free Resource?',
            'is_official': 'Official Resource?',
            'is_trending': 'Trending?',
        }


class CourseFilterForm(forms.Form):
    """Form for filtering courses"""
    
    LEVEL_CHOICES = [
        ('', 'All Levels'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    SORT_CHOICES = [
        ('-created_at', 'Newest First'),
        ('name', 'Name (A-Z)'),
        ('level', 'Level (Beginner → Advanced)'),
        ('-updated_at', 'Recently Updated'),
    ]
    
    category = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by category'
        })
    )
    
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
