from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Purchase(models.Model):
    purchaser_name = models.CharField(max_length=50)
    quantity = models.IntegerField()


class PurchaseStatus(models.Model):
    status_choices = (
        ('open', 'Open'),
        ('verified', 'Verified'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
    )
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=status_choices)
    created_at = models.DateTimeField(default=timezone.now)
