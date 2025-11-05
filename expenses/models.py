from django.db import models
import requests

def convert_to_usd(amount, currency):
    if currency == "USD":
        return amount
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url).json()
        rate = response['rates'].get(currency)
        return round(amount / rate, 2) if rate else amount
    except:
        return amount

class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    date = models.DateField()
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.usd_amount = convert_to_usd(self.amount, self.currency)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.amount} {self.currency}"