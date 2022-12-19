from django.core.management.base import BaseCommand
from account_management_app.models import ExternalLedgerMetadata, Account

import requests
import kronos

@kronos.register('* * * * *')
class Command(BaseCommand):
    def handle(self, *args, **options):
        to_be_created_transactions = ExternalLedgerMetadata.objects.filter(status='to_be_confirmed')
        
        for transaction in to_be_created_transactions:
            # If receiver doesn't exist, cancel locally
            receiver_account = Account.objects.get(account_number=transaction.receiver_account_number)
            
            if receiver_account:
                # Update status to confirmed
                transaction.status = 'confirmed'
                transaction.save()
                # Create entry in local ledger
                transaction.reservation_bank_account.make_payment(transaction.amount, transaction.receiver_account_number)
                print(f'Transaction finished for transfer with ID: {transaction.token}')
            else:
                print(f'Receiver does not exist, cancelling transaction with ID: {transaction.token}')
                # Abort locally
                transaction.status = 'cancelled'
                transaction.save()

                # And abort transaction by calling update state to cancel
                external_bank_url = transaction.reservation_bank_account.bank.api_url
                url = external_bank_url+f'/api/v1/transaction/{transaction.token}/'
                # From receiver to reservation
                requests.put(url, data = {'status': 'to_be_deleted' })
            