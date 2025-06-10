from django.db import models
from django.contrib.auth.models import User


class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    asset_name = models.CharField(max_length=100)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    @property
    def profit_loss(self):
        return self.current_value - self.amount_invested

    @property
    def profit_loss_percentage(self):
        if self.amount_invested > 0:
            return (self.profit_loss / self.amount_invested) * 100
        return 0

class TransactionLog(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('PURCHASE', 'Purchase'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.transaction_type} – {self.reference_id}"
