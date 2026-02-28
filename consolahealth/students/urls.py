from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('background/', views.background_view, name='background'),
    path('create/', views.create_view, name='create'),
    path('create_student/', views.create_student, name='create_student'),
    path('edit/<int:student_id>/', views.edit_view, name='edit'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<int:student_id>/', views.delete_view, name='delete'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
]