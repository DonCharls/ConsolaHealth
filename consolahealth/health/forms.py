from django import forms
from .models import HealthRecord
from students.models import Student

class HealthRecordForm(forms.ModelForm):
    """Form for recording health check-ups with Bootstrap 5 styling"""
    
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select Student'
        }),
        label="Student"
    )
    
    class Meta:
        model = HealthRecord
        fields = ['student', 'weight', 'height', 'systolic_bp', 'diastolic_bp', 
                  'temperature', 'vision', 'urine_test', 'school_year']
        widgets = {
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight (kg)',
                'step': '0.01',
                'min': '0'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Height (cm)',
                'step': '0.01',
                'min': '0'
            }),
            'systolic_bp': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Systolic (mmHg)',
                'min': '0'
            }),
            'diastolic_bp': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Diastolic (mmHg)',
                'min': '0'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Temperature (°C)',
                'step': '0.1',
                'min': '0'
            }),
            'vision': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 20/20',
            }),
            'urine_test': forms.Select(attrs={
                'class': 'form-select',
            }),
            'school_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2024-2025',
            }),
        }
        labels = {
            'weight': 'Weight (kg)',
            'height': 'Height (cm)',
            'systolic_bp': 'Systolic BP (mmHg)',
            'diastolic_bp': 'Diastolic BP (mmHg)',
            'temperature': 'Temperature (°C)',
            'vision': 'Vision Test Result',
            'urine_test': 'Urine Test',
            'school_year': 'School Year',
        }


class StudentSearchForm(forms.Form):
    """Form for searching students"""
    search = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by Student ID, First Name, or Last Name',
        }),
        label="Search Student"
    )
