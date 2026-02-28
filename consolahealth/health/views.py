from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Avg, Count, Q, F
from django.contrib import messages
from django.utils import timezone
from students.models import Student
from .models import HealthRecord
from .forms import HealthRecordForm, StudentSearchForm
import json
from datetime import datetime, timedelta

class HealthDashboardView(TemplateView):
    """Dashboard view with summary statistics and data for graphs"""
    template_name = 'health/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all students for the modal dropdown
        all_students = Student.objects.all().order_by('last_name', 'first_name')
        context['students'] = all_students
        
        # Get all health records
        all_records = HealthRecord.objects.all()
        
        # Total students with health records
        total_students = all_records.values('student').distinct().count()
        context['total_students'] = total_students
        
        # Average BMI
        avg_bmi = 0
        if all_records.exists():
            bmi_sum = sum([record.bmi for record in all_records if record.bmi])
            bmi_count = len([record.bmi for record in all_records if record.bmi])
            avg_bmi = round(bmi_sum / bmi_count, 2) if bmi_count > 0 else 0
        context['avg_bmi'] = avg_bmi
        
        # Health Category Distribution
        health_distribution = {'underweight': 0, 'normal': 0, 'overweight': 0, 'obese': 0}
        for record in all_records:
            category = record.health_category
            if category in health_distribution:
                health_distribution[category] += 1
        
        context['health_distribution_data'] = json.dumps(health_distribution)
        
        # Average Weight per School Year
        school_years = all_records.values('school_year').distinct().order_by('school_year')
        weight_by_year = {}
        for year_data in school_years:
            year = year_data['school_year']
            avg_weight = all_records.filter(school_year=year).aggregate(
                avg=Avg('weight')
            )['avg']
            weight_by_year[year] = float(avg_weight) if avg_weight else 0
        
        context['weight_by_year_data'] = json.dumps(weight_by_year)
        
        # Recent Check-ups
        recent_records = HealthRecord.objects.select_related('student').order_by('-checkup_date')[:10]
        context['recent_records'] = recent_records
        
        # Student count per year
        students_per_year = {}
        for year_data in school_years:
            year = year_data['school_year']
            count = all_records.filter(school_year=year).values('student').distinct().count()
            students_per_year[year] = count
        
        context['students_per_year'] = json.dumps(students_per_year)
        
        return context




class StudentHealthHistoryView(View):
    """View showing a specific student's health progress over time"""
    template_name = 'health/student_health_history.html'
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        health_records = HealthRecord.objects.filter(student=student).order_by('-checkup_date')
        
        # Prepare data for charts
        weights = [float(record.weight) for record in health_records]
        bmis = [record.bmi for record in health_records]
        dates = [record.checkup_date.strftime('%Y-%m-%d') for record in health_records]
        
        context = {
            'student': student,
            'health_records': health_records,
            'weights_data': json.dumps(weights),
            'bmis_data': json.dumps(bmis),
            'dates_data': json.dumps(dates),
            'latest_record': health_records.first() if health_records.exists() else None,
        }
        
        return render(request, self.template_name, context)


class AllRecordsView(TemplateView):
    """View showing all health records with filtering and search"""
    template_name = 'health/all_records.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get search and filter parameters
        search_query = self.request.GET.get('search', '')
        course_filter = self.request.GET.get('course', '')
        year_filter = self.request.GET.get('year', '')
        category_filter = self.request.GET.get('category', '')
        
        # Start with all records
        records = HealthRecord.objects.select_related('student').order_by('-checkup_date')
        
        # Apply filters
        if search_query:
            records = records.filter(
                Q(student__first_name__icontains=search_query) |
                Q(student__last_name__icontains=search_query) |
                Q(student__s_id__icontains=search_query)
            )
        
        if course_filter:
            records = records.filter(student__department=course_filter)
        
        if year_filter:
            records = records.filter(school_year=year_filter)
        
        if category_filter:
            records = records.filter(
                weight__isnull=False,
                height__isnull=False
            )
            # Filter by health category in Python
            filtered_records = []
            for record in records:
                if record.health_category == category_filter:
                    filtered_records.append(record)
            records = filtered_records
        
        # Get available options for filters
        all_courses = Student.DEPARTMENT_CHOICES
        all_years = HealthRecord.objects.values_list('school_year', flat=True).distinct().order_by('-school_year')
        
        context['health_records'] = records
        context['total_records'] = len(records) if isinstance(records, list) else records.count()
        context['courses'] = all_courses
        context['school_years'] = all_years
        context['current_search'] = search_query
        context['current_course_filter'] = course_filter
        context['current_year_filter'] = year_filter
        context['current_category_filter'] = category_filter
        
        return context


class CreateHealthRecordView(View):
    """View to create a new health record from the dashboard"""
    
    def post(self, request):
        # Get form data from request.POST
        student_id = request.POST.get('student')
        checkup_date = request.POST.get('checkup_date')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        systolic_bp = request.POST.get('systolic_bp')
        diastolic_bp = request.POST.get('diastolic_bp')
        temperature = request.POST.get('temperature')
        vision = request.POST.get('vision')
        urine_test = request.POST.get('urine_test')
        
        try:
            student = get_object_or_404(Student, pk=student_id)
            
            # Create health record
            health_record = HealthRecord.objects.create(
                student=student,
                checkup_date=checkup_date if checkup_date else timezone.now().date(),
                weight=float(weight) if weight else 0,
                height=float(height) if height else 0,
                systolic_bp=int(systolic_bp) if systolic_bp else 0,
                diastolic_bp=int(diastolic_bp) if diastolic_bp else 0,
                temperature=float(temperature) if temperature else 0,
                vision=vision if vision else '',
                urine_test=urine_test if urine_test else '',
                school_year=timezone.now().year
            )
            
            messages.success(request, f"Health record for {student.first_name} {student.last_name} added successfully!")
            return redirect('health:dashboard')
        except (ValueError, TypeError) as e:
            messages.error(request, f"Error creating health record: {str(e)}")
            return redirect('health:dashboard')


class EditHealthRecordView(View):
    """View to edit an existing health record"""
    
    def post(self, request, record_id):
        record = get_object_or_404(HealthRecord, pk=record_id)
        form = HealthRecordForm(request.POST, instance=record)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Health record updated successfully!")
            return redirect('health:student_history', student_id=record.student.id)
        else:
            messages.error(request, "Please correct the errors below.")
            return redirect('health:student_history', student_id=record.student.id)


class DeleteHealthRecordView(View):
    """View to delete a health record"""
    
    def post(self, request, record_id):
        record = get_object_or_404(HealthRecord, pk=record_id)
        student_id = record.student.id
        record.delete()
        messages.success(request, "Health record deleted successfully!")
        return redirect('health:student_history', student_id=student_id)
