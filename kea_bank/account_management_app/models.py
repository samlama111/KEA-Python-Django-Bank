from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.db.models import Sum

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
        max_length=10,
        choices=CustomerRank.choices,
        default=CustomerRank.BASIC
    )


class Account(models.Model):
    account_number = models.IntegerField(unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    class AccountType(models.TextChoices):
        PRIVATE='private'
        BUSINESS='business'
        LOAN='loan'
        BANK='bank'

    account_type = models.CharField(
        max_length=10,
        choices=AccountType.choices,
        default=AccountType.PRIVATE
    )

    def get_transactions(self):
        my_transactions = Ledger.objects.filter(account=self)
        return my_transactions

    @property
    def balance(self):
        my_transactions = self.get_transactions()
        if my_transactions.count() == 0:
            return 0
        my_transactions_with_balance = my_transactions.aggregate(balance=Sum("amount"))
        return my_transactions_with_balance['balance']
    
    
    def make_payment(self, amount, account_number):
        # TODO: replace 9999 with bank's account number
        if self.balance < int(amount) and self.account_number != 9999:
            raise ValidationError('Balance is too low')

        target_account = Account.objects.get(account_number=account_number)

        with transaction.atomic():
            Ledger.objects.create(account=target_account, is_creditor=True, amount=int(amount), note='', variable_symbol='')
            Ledger.objects.create(account=self, is_creditor=False, amount=-int(amount), note='', variable_symbol='')
    

class Ledger(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    is_creditor = models.BooleanField(default=False)
    amount = models.IntegerField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=100)
    variable_symbol = models.CharField(max_length=30)

    