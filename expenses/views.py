# expenses/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework import generics
from .models import Expense
from .serializers import ExpenseSerializer
from .utils import get_monthly_totals
import json


# ---------- API ----------
class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer


# ---------- HTML UI ----------
class DashboardView(ListView):
    template_name = 'expenses/dashboard.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        return Expense.objects.all().order_by('-date')[:10]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        totals = get_monthly_totals()
        ctx['chart_labels'] = json.dumps([m['month'] for m in totals])
        ctx['chart_data']   = json.dumps([float(m['total_usd']) for m in totals])
        return ctx


class ExpenseListView(ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    ordering = ['-date']
    paginate_by = 20


class ExpenseCreateView(CreateView):
    model = Expense
    template_name = 'expenses/expense_form.html'
    fields = ['title', 'amount', 'currency', 'date']
    success_url = reverse_lazy('expense-list')


class ExpenseUpdateView(UpdateView):
    model = Expense
    template_name = 'expenses/expense_form.html'
    fields = ['title', 'amount', 'currency', 'date']
    success_url = reverse_lazy('expense-list')


class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')