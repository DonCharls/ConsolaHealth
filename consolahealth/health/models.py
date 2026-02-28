from django.db import models
from students.models import Student
from decimal import Decimal

class HealthRecord(models.Model):
    """Health Record for students with vital signs and measurements"""
    
    HEALTH_CATEGORY_CHOICES = [
        ('underweight', 'Underweight'),
        ('normal', 'Normal Weight'),
        ('overweight', 'Overweight'),
        ('obese', 'Obese'),
    ]
    
    URINE_TEST_CHOICES = [
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal'),
        ('pending', 'Pending'),
    ]

    # Foreign Key
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='health_records')
    
    # Measurements
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    
    # Vital Signs
    systolic_bp = models.IntegerField(help_text="Systolic Blood Pressure (mmHg)")
    diastolic_bp = models.IntegerField(help_text="Diastolic Blood Pressure (mmHg)")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text="Temperature in °C")
    
    # Health Tests
    vision = models.CharField(max_length=50, blank=True, null=True, help_text="Vision test result (e.g., 20/20)")
    urine_test = models.CharField(max_length=20, choices=URINE_TEST_CHOICES, default='pending')
    
    # Metadata
    school_year = models.CharField(max_length=9, blank=True, null=True, help_text="e.g., 2024-2025")
    checkup_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-checkup_date']
        verbose_name = 'Health Record'
        verbose_name_plural = 'Health Records'

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.school_year}"
    
    @property
    def bmi(self):
        """Calculate BMI (Body Mass Index) = weight(kg) / (height(m))^2"""
        height_m = float(self.height) / 100  # Convert cm to meters
        if height_m > 0:
            bmi_value = float(self.weight) / (height_m ** 2)
            return round(bmi_value, 2)
        return None
    
    @property
    def health_category(self):
        """Determine health category based on BMI"""
        if self.bmi is None:
            return 'unknown'
        if self.bmi < 18.5:
            return 'underweight'
        elif 18.5 <= self.bmi < 25:
            return 'normal'
        elif 25 <= self.bmi < 30:
            return 'overweight'
        else:
            return 'obese'
    
    @property
    def bp_status(self):
        """Determine blood pressure status"""
        systolic = self.systolic_bp
        diastolic = self.diastolic_bp
        
        if systolic < 120 and diastolic < 80:
            return 'Normal'
        elif systolic < 130 and diastolic < 80:
            return 'Elevated'
        elif systolic < 140 and diastolic < 90:
            return 'Stage 1 Hypertension'
        else:
            return 'Stage 2 Hypertension'
