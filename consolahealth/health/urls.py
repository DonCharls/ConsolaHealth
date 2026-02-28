from django.urls import path
from . import views

app_name = 'health'

urlpatterns = [
    path('dashboard/', views.HealthDashboardView.as_view(), name='dashboard'),
    path('add-record/', views.CreateHealthRecordView.as_view(), name='add_record'),
    path('all-records/', views.AllRecordsView.as_view(), name='all_records'),
    path('student/<int:student_id>/history/', views.StudentHealthHistoryView.as_view(), name='student_history'),
    path('record/<int:record_id>/edit/', views.EditHealthRecordView.as_view(), name='edit_record'),
    path('record/<int:record_id>/delete/', views.DeleteHealthRecordView.as_view(), name='delete_record'),
]
