from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Student
import json

# 1. The Home View (Displaying the List)
def home(request):
    # We use lowercase 'students' to match your template loop: {% for x in students %}
    students = Student.objects.all()
    
    # Calculate department distribution
    departments = dict(Student.DEPARTMENT_CHOICES)
    dept_counts = {}
    for code, name in Student.DEPARTMENT_CHOICES:
        count = students.filter(department=code).count()
        dept_counts[code] = {
            'name': name,
            'count': count
        }
    
    # Calculate year level distribution
    year_levels = dict(Student.YEAR_LEVEL_CHOICES)
    year_counts = {}
    for code, name in Student.YEAR_LEVEL_CHOICES:
        count = students.filter(year_level=code).count()
        year_counts[code] = {
            'name': name,
            'count': count
        }
    
    # Prepare chart data
    dept_labels = [code for code, _ in Student.DEPARTMENT_CHOICES]
    dept_data = [dept_counts[code]['count'] for code, _ in Student.DEPARTMENT_CHOICES]
    
    year_labels = [year_counts[code]['name'] for code, _ in Student.YEAR_LEVEL_CHOICES]
    year_data = [year_counts[code]['count'] for code, _ in Student.YEAR_LEVEL_CHOICES]
    
    context = {
        'students': students,
        'dept_labels': json.dumps(dept_labels),
        'dept_data': json.dumps(dept_data),
        'year_labels': json.dumps(year_labels),
        'year_data': json.dumps(year_data),
    }
    return render(request, 'home.html', context)

# 2. The View to show the Create Form
def create_view(request):
    return render(request, 'create.html')

# 3. The Action that saves the data
def create_student(request):
    if request.method == 'POST':
        # Retrieve data using the NEW 'name' attributes from your HTML form
        s_id = request.POST.get('s_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        year_level = request.POST.get('year_level')

        # Validation: Ensure the main fields aren't empty
        if s_id and first_name and last_name and department:
            Student.objects.create(
                s_id=s_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                department=department,
                year_level=year_level
            )
            messages.success(request, f'Student {first_name} {last_name} created successfully!')
            return redirect('home') # Use the name of your URL route
        
        return render(request, 'create.html', {"error": "All fields are required"})
    
    return redirect('home')

# 4. Edit Student View
def edit_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'edit.html', {'student': student})

# 5. Update Student Data
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        # Retrieve data from form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        year_level = request.POST.get('year_level')

        # Validation: Ensure the main fields aren't empty
        if first_name and last_name and department:
            student.first_name = first_name
            student.last_name = last_name
            student.email = email
            student.department = department
            student.year_level = year_level
            student.save()
            messages.success(request, f'Student {first_name} {last_name} updated successfully!')
            return redirect('home')
        
        messages.error(request, 'All required fields must be filled.')
        return render(request, 'edit.html', {'student': student, 'error': 'All fields are required'})
    
    return redirect('home')

# 6. Delete Student View (Confirmation)
def delete_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'delete.html', {'student': student})

# 7. Delete Student Action
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student_name = f'{student.first_name} {student.last_name}'
        student.delete()
        messages.success(request, f'Student {student_name} deleted successfully!')
        return redirect('home')
    
    return redirect('home')

# 8. Background Animation View
def background_view(request):
    return render(request, 'background.html')