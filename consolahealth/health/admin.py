from django.contrib import admin
from .models import HealthRecord

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'school_year', 'checkup_date', 'bmi', 'health_category', 'bp_status')
    list_filter = ('school_year', 'urine_test')
    search_fields = ('student__first_name', 'student__last_name', 'student__s_id')
    readonly_fields = ('checkup_date', 'last_updated', 'bmi', 'health_category', 'bp_status')
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Measurements', {
            'fields': ('weight', 'height', 'bmi')
        }),
        ('Vital Signs', {
            'fields': ('systolic_bp', 'diastolic_bp', 'bp_status', 'temperature')
        }),
        ('Health Tests', {
            'fields': ('vision', 'urine_test')
        }),
        ('Metadata', {
            'fields': ('school_year', 'health_category', 'checkup_date', 'last_updated')
        }),
    )
    
    def bmi(self, obj):
        return f"{obj.bmi} kg/m²" if obj.bmi else "N/A"
    bmi.short_description = "BMI"
    
    def health_category(self, obj):
        return obj.health_category.upper()
    health_category.short_description = "Health Category"
    
    def bp_status(self, obj):
        return obj.bp_status
    bp_status.short_description = "Blood Pressure Status"
