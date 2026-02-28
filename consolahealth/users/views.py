from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def users(request): 
    return HttpResponse(" Here are the List of Users")

def register(request):
    return render(request, 'register.html')

def profile(request):
    return HttpResponse(" Your Profile")