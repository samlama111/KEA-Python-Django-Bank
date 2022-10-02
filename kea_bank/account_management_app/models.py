import uuid
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

    @property
    def total_balance(self):
        accounts = Account.objects.filter(customer=self)
        total_balance = 0
        for item in accounts:
            total_balance += item.balance
        return total_balance


class Account(models.Model):
    account_number = models.IntegerField(unique=True)
    is_customer = models.BooleanField(default=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    class AccountType(models.TextChoices):
        PRIVATE='private'
        BUSINESS='business'
        LOAN='loan'

    account_type = models.CharField(
        max_length=10,
        choices=AccountType.choices,
        default=AccountType.PRIVATE
    )

    def get_transactions(self):
        my_transactions = Ledger.objects.filter(account=self)
        return my_transactions

    def get_loan_transactions(self):
        loan_transactions = Ledger.objects.filter(account=self, is_loan=True)
        return loan_transactions

    def get_amount_owed(self):
        loan_transactions = self.get_loan_transactions()
        if loan_transactions.count() == 0:
            return 0
        my_loan_transactions_with_balance = loan_transactions.aggregate(balance=Sum("amount"))
        return my_loan_transactions_with_balance['balance']

    @property
    def balance(self):
        my_transactions = self.get_transactions()
        if my_transactions.count() == 0:
            return 0
        my_transactions_with_balance = my_transactions.aggregate(balance=Sum("amount"))
        return my_transactions_with_balance['balance']
    

    def make_payment(self, amount, account_number, is_loan=False):
        if is_loan==False and self.balance < int(amount):
            raise ValidationError('Balance is too low')

        target_account = Account.objects.get(account_number=account_number)

        with transaction.atomic():
            transaction_id = uuid.uuid4()
            Ledger.objects.create(account=target_account, is_creditor=True, amount=int(amount), transaction_id=transaction_id, is_loan=is_loan, note='', variable_symbol='')
            Ledger.objects.create(account=self, is_creditor=False, amount=-int(amount), transaction_id=transaction_id, note='', is_loan=is_loan, variable_symbol='')
    

class Ledger(models.Model):
    transaction_id = models.UUIDField(default = uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    is_creditor = models.BooleanField(default=False)
    is_loan = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=15, decimal_places=4)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=100)
    variable_symbol = models.CharField(max_length=30)

    class Meta:
        unique_together = ['transaction_id', 'account']
    