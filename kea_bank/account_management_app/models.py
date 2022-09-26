from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # reached using user.customer https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-the-existing-user-model
    phone_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)

    class CustomerRank(models.TextChoices):
        BASIC='basic'
        SILVER='silver'
        GOLD='gold'

    rank = models.CharField(
        choices=CustomerRank.choices,
        default=CustomerRank.BASIC
    )

# Create your models here.
