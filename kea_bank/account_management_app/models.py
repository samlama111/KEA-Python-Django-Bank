import uuid
from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.exceptions import ValidationError

class Bank(models.Model):
    bank_id = models.IntegerField(editable=False, primary_key=True)
    name = models.CharField(max_length=50)
    api_url = models.CharField(max_length=50)
    
    class BankType(models.TextChoices):
        LOCAL='local'
        EXTERNAL='external'

    bank_type = models.CharField(
        max_length=10,
        choices=BankType.choices,
        default=BankType.EXTERNAL
    )

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # reached using user.customer https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-the-existing-user-model
    phone_number = models.CharField(max_length=10)

    class CustomerRank(models.TextChoices):
        BASIC='basic'
        SILVER='silver'
        GOLD='gold'

    rank = models.CharField(
        max_length=10,
        choices=CustomerRank.choices,
        default=CustomerRank.BASIC
    )

    def get_accounts(self):
        return Account.objects.filter(user=self.user)
    
    def get_external_banks(self):    
        return Bank.objects.filter(bank_type='external')

    def get_bank_operational_account(self):
        return Account.objects.get(account_type='operational')
    
    @property
    def total_balance(self):
        accounts = self.get_accounts()
        total_balance = 0
        for item in accounts:
            total_balance += item.balance
        return total_balance
    
    @property
    def total_balance_bank_accounts(self):
        accounts = Account.objects.filter(user=self.user, is_saving_account = False)
        total_balance = 0
        for item in accounts:
            total_balance += item.balance
        return total_balance
    
    @property
    def total_balance_saving_accounts(self):
        accounts = Account.objects.filter(user=self.user, is_saving_account = True)
        total_balance = 0
        for item in accounts:
            total_balance += item.balance
        return total_balance


class Account(models.Model):
    account_number = models.AutoField(primary_key=True)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    is_saving_account=models.BooleanField(default=False)
    
    class AccountType(models.TextChoices):
        CUSTOMER='customer'
        LOAN='loan'
        OPERATIONAL='operational'

    account_type = models.CharField(
        max_length=15,
        choices=AccountType.choices,
        default=AccountType.CUSTOMER
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
    
    def get_saving_account_transactions(self):
        saving_account_transactions = Ledger.objects.filter(account=self, is_saving_account = True)
        return saving_account_transactions
    
    @property
    def saving_account_balance(self):
        saving_transaction = self.get_saving_account_transactions()
        if saving_transaction.count() == 0:
            return 0
        saving_transaction_with_balance = saving_transaction.aggregate(balance=Sum("amount"))
        return saving_transaction_with_balance['balance']


    @property
    def balance(self):
        my_transactions = self.get_transactions()
        if my_transactions.count() == 0:
            return 0
        my_transactions_with_balance = my_transactions.aggregate(balance=Sum("amount"))
        return my_transactions_with_balance['balance']
    

    def make_payment(self, amount, account_number, is_loan=False, is_saving_account=False):
        if amount < 0:
            raise ValidationError('Please use a positive amount')

        if is_loan==False and self.balance < int(amount):
            raise ValidationError('Balance is too low')

        target_account = Account.objects.get(account_number=account_number)

        with transaction.atomic():
            transaction_id = uuid.uuid4()
            Ledger.objects.create(account=target_account, is_creditor=True, amount=int(amount), transaction_id=transaction_id, is_loan=is_loan, note='', variable_symbol='', is_saving_account=is_saving_account)
            Ledger.objects.create(account=self, is_creditor=False, amount=-int(amount), transaction_id=transaction_id, note='', is_loan=is_loan, variable_symbol='', is_saving_account=is_saving_account)
    

class Ledger(models.Model):
    transaction_id = models.UUIDField(default = uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_creditor = models.BooleanField(default=False)
    is_loan = models.BooleanField(default=False)
    is_saving_account = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=15, decimal_places=4)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=100)
    variable_symbol = models.CharField(max_length=30)

    class Meta:
        unique_together = ['transaction_id', 'account']

class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    json_array = models.JSONField(default=dict, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
 
class ExternalLedgerMetadata(models.Model):
    token = models.UUIDField(default = uuid.uuid4)
    reservation_bank_account = models.ForeignKey(Account, on_delete=models.PROTECT)
    sender_account_number = models.IntegerField()
    receiver_account_number = models.IntegerField()
    amount = models.DecimalField(max_digits=15, decimal_places=4)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    
    class StatusType(models.TextChoices):
        PENDING='pending'
        IN_PROGRESS='in_progress'
        TO_BE_CONFIRMED='to_be_confirmed'
        TO_BE_DELETED='to_be_deleted'
        CONFIRMED='confirmed'
        CANCELLED='cancelled'

    status = models.CharField(
        max_length=15,
        choices=StatusType.choices,
        default=StatusType.PENDING
    )
