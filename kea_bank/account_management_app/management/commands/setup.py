from decimal import Decimal
import secrets
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from account_management_app.models import Account, Customer, Bank
from employee_app.models import Employee


class Command(BaseCommand):
    help = 'Sets up the banks accounts'

    def handle(self, **options):
        print('Adding demo data ...')

        # bank entity created
        bank = Bank.objects.create(bank_id=1000,
                                   name="Default bank",
                                   api_url="http://localhost:8000",
                                   bank_type='local')

        bank_user = User.objects.create_user(
            'bank', email='', password=secrets.token_urlsafe(64))
        bank_user.is_active = False
        bank_user.save()

        ops_account = Account.objects.create(user=bank_user,
                                             bank=bank,
                                             name='Bank Operational Account',
                                             account_type='operational')
        ipo_account = Account.objects.create(user=bank_user,
                                             bank=bank,
                                             name='Bank Investment Account',
                                             account_type='loan')
        ipo_account.make_payment(
            Decimal(10_000_000),
            ops_account.account_number,
            is_loan=True,
        )

        default_user = User.objects.create_user('user',
                                                email='t',
                                                password='test123')
        default_user.first_name = 'Default'
        default_user.last_name = 'User'
        default_user.save()

        default_customer = Customer(user=default_user,
                                    phone_number='555666',
                                    rank='silver')
        default_customer.save()

        default_account = Account.objects.create(user=default_user,
                                                 bank=bank,
                                                 name='Checking account')
        default_account.save()

        # External account set-up
        external_bank = Bank.objects.create(bank_id=1001,
                                            name="External bank",
                                            api_url="http://localhost:3001")

        external_bank_user = User.objects.create_user(
            'External bank', email='', password=secrets.token_urlsafe(64))
        external_bank_user.is_active = False
        external_bank_user.save()

        local_external_account = Account.objects.create(
            user=external_bank_user,
            bank=external_bank,
            name='External Bank Operational Account',
            account_type='loan')

        default_user_employee = User.objects.create_user(
            'employee', email='employee@gmail.com', password='test123')
        default_user_employee.first_name = 'Default Employee'
        default_user_employee.last_name = 'Employee'
        default_user_employee.save()

        default_employee = Employee(user=default_user_employee)
        default_employee.save()
