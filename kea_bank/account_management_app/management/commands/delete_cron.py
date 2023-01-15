from django.core.management.base import BaseCommand
from account_management_app.models import ExternalLedgerMetadata, Account

import kronos

@kronos.register('* * * * *')
class Command(BaseCommand):
    def handle(self, *args, **options):
        to_be_deleted_transactions = ExternalLedgerMetadata.objects.filter(status='to_be_deleted')
        
        # Locally revert all transactions        
        for transaction in to_be_deleted_transactions:
            # negate reservation transaction in Ledger table
            transaction.reservation_bank_account.make_payment(transaction.amount, transaction.sender_account_number, is_loan=True)
            
            # set status to cancelled, 
            transaction.status = 'cancelled'
            transaction.save()
            
            print(f'Transaction deleted with ID: {transaction.token}')