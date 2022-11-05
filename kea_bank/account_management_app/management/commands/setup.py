import secrets
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from account_management_app.models import Account

class Command(BaseCommand):
    help = 'Sets up the banks accounts'
    
    def handle(self, **options):
        print('Adding demo data ...')

        # bank entity created
        bank_user = User.objects.create_user('bank', email='', password=secrets.token_urlsafe(64))
        bank_user.is_active = False
        bank_user.save()
        
        ops_account = Account.objects.create(user=bank_user, is_customer=False, name='Bank Operational Account')
        ipo_account = Account.objects.create(user=bank_user, is_customer=False, name='Bank Investment Account')
        ipo_account.make_payment(
            10_000_000,
            ops_account.account_number,
            is_loan=True
        )
