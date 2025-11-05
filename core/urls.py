# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('expenses.urls')),          # REST API
    path('dashboard/', include('expenses.urls')),    # HTML dashboard
]