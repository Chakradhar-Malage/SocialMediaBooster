# expenses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # API
    path('expenses/', views.ExpenseListCreateAPIView.as_view(), name='api-expense-list'),

    # HTML UI
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('expenses/list/', views.ExpenseListView.as_view(), name='expense-list'),
    path('expenses/add/', views.ExpenseCreateView.as_view(), name='expense-add'),
    path('expenses/<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='expense-edit'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense-delete'),
]