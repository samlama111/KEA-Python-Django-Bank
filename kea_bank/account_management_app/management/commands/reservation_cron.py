from django.core.management.base import BaseCommand
from account_management_app.models import ExternalLedgerMetadata, Bank

import kronos
import requests

@kronos.register('* * * * *')
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Get all pending transactions in External Ledger Table
        pending_transactions = ExternalLedgerMetadata.objects.filter(status='pending')
        
        # Make POST request to bank API to create a reservation
        for transaction in pending_transactions:
            # TODO: add check how old the transaction is
            print(f'Creating reservation for transfer with ID: {transaction.id}')
            external_bank_url = transaction.receiver_account.bank.api_url
            # External bank's operation account is 1, sender's account is hardcoded to 4
            myobj = {'amount': int(transaction.amount), 'receiver_account': 1, 'sender_account': 4}
            res = requests.post(external_bank_url+'/api/v1/transaction', data = myobj)
            if (res.status_code == 201):  
                print(f'Reservation created for transfer with ID: {transaction.id}')
            else:
                print(f'Reservation failed for transfer with ID: {transaction.id}')