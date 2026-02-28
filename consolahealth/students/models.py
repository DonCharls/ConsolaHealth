from django.db import models
from django.utils import timezone

class Student(models.Model):
    # --- CHOICES CONFIGURATION ---
    # The first item is stored in DB, the second is what users see in the form
    DEPARTMENT_CHOICES = [
        ('BSIT', 'Bachelor of Science in Information Technology'),
        ('BSED', 'Bachelor of Secondary Education'),
        ('BEED', 'Bachelor of Elementary Education'),
        ('BSHM', 'Bachelor of Science in Hospitality Management'),
        ('BPEd', 'Bachelor of Physical Education'),
        ('BSEntrep', 'Bachelor of Science in Entrepreneurship'),
    ]

    YEAR_LEVEL_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    # --- DATABASE FIELDS ---
    s_id = models.IntegerField(unique=True, verbose_name="Student ID") # unique=True prevents duplicates
    
    # Personal Information
    first_name = models.CharField(max_length=64)
    middle_initial = models.CharField(max_length=5, blank=True, null=True) # Optional field
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    
    # Contact Information
    address = models.TextField(verbose_name="Home Address") # TextField is better for long addresses
    email = models.EmailField(blank=True, null=True)
    
    # Academic Information
    department = models.CharField(
        max_length=10, 
        choices=DEPARTMENT_CHOICES, 
        default='BSIT'
    )
    year_level = models.CharField(
        max_length=1, 
        choices=YEAR_LEVEL_CHOICES, 
        default='1'
    )

    # System Logs (Automatic)
    created_at = models.DateTimeField(auto_now_add=True) # Sets time only when created
    updated_at = models.DateTimeField(auto_now=True)     # Updates time every save

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.s_id})"