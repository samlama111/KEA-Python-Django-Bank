import secrets
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from account_management_app.models import Account, Customer
from employee_app.models import Employee

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
            is_loan=True,
            is_saving_account=False
        )

        default_user = User.objects.create_user('user', email='t', password='test123')
        default_user.first_name = 'Default'
        default_user.last_name  = 'User'
        default_user.save()
        
        default_customer = Customer(user=default_user, phone_number='555666', rank='silver')
        default_customer.save()
        
        default_account = Account.objects.create(user=default_user, name='Checking account', is_customer=True)
        default_account.save()

        default_user_employee = User.objects.create_user('employee', email='employee@gmail.com', password='test123')
        default_user_employee.first_name = 'Default Employee'
        default_user_employee.last_name  = 'Employee'
        default_user_employee.save()

        default_employee=Employee(user=default_user_employee)
        default_employee.save()

        