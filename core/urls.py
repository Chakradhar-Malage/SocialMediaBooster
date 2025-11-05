# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect('dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('expenses.urls')),
    path('', home, name='home'),                 # ← root → dashboard
    path('', include('expenses.urls')),          # dashboard + CRUD pages
]