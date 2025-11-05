# expenses/utils.py
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from datetime import datetime
from .models import Expense


def get_monthly_totals():
    """Return list of dicts: [{'month': '2025-11', 'total_usd': 123.45}, …]"""
    expenses = Expense.objects.all()
    totals = {}
    for exp in expenses:
        month_key = exp.date.strftime('%Y-%m')
        totals.setdefault(month_key, 0)
        totals[month_key] += exp.usd_amount

    # Sort by month
    sorted_items = sorted(totals.items())
    return [{'month': m, 'total_usd': round(v, 2)} for m, v in sorted_items]