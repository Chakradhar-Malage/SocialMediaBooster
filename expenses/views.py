from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Sum
from .models import Expense
from .serializers import ExpenseSerializer
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-created_at')
    serializer_class = ExpenseSerializer

@api_view(['GET'])
def dashboard(request):
    today = timezone.now().date()
    start_date = today - relativedelta(months=5)  # Last 6 months
    expenses = Expense.objects.filter(date__gte=start_date).extra(
        select={'month': "EXTRACT(month FROM date)"}
    ).values('month').annotate(total=Sum('usd_amount')).order_by('month')
    
    months = []
    amounts = []
    for exp in expenses:
        month_num = int(exp['month'])
        month_name = calendar.month_abbr[month_num]
        months.append(month_name)
        amounts.append(float(exp['total'] or 0))
    
    # Fill missing months
    current_month = start_date.month
    while current_month <= today.month:
        if not any(m == calendar.month_abbr[current_month] for m in months):
            months.insert(0, calendar.month_abbr[current_month])
            amounts.insert(0, 0)
        current_month += 1
    
    context = {
        'months': months,
        'amounts': amounts,
    }
    return render(request, 'dashboard.html', context)