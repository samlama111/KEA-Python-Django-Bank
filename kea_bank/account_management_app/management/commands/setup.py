import secrets
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from account_management_app.models import Account, Customer, Bank

class Command(BaseCommand):
    help = 'Sets up the banks accounts'
    
    def handle(self, **options):
        print('Adding demo data ...')

        # bank entity created
        bank = Bank.objects.create(bank_id=1000, name="Default bank", api_url="http://localhost:3000", bank_type='local')
        
        bank_user = User.objects.create_user('bank', email='', password=secrets.token_urlsafe(64))
        bank_user.is_active = False
        bank_user.save()
        
        ops_account = Account.objects.create(user=bank_user, bank=bank, name='Bank Operational Account', account_type='operational')
        ipo_account = Account.objects.create(user=bank_user, bank=bank, name='Bank Investment Account', account_type='loan')
        ipo_account.make_payment(
            10_000_000,
            ops_account.account_number,
            is_loan=True
        )

        default_user = User.objects.create_user('user', email='user@dummy.com', password='test123')
        default_user.first_name = 'Default'
        default_user.last_name  = 'User'
        default_user.save()
        
        default_customer = Customer(user=default_user, phone_number='555666', rank='silver')
        default_customer.save()
        
        default_account = Account.objects.create(user=default_user, bank=bank, name='Checking account')
        default_account.save()

        