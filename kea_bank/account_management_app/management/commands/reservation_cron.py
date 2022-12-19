from django.core.management.base import BaseCommand
from account_management_app.models import ExternalLedgerMetadata, Account

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
            external_bank_url = transaction.reservation_bank_account.bank.api_url
            external_bank_metadata = {
                'amount': int(transaction.amount),
                'receiver_account_number': transaction.receiver_account_number, 
                'sender_account_number': transaction.sender_account_number,
                # Local bank's ID in external bank is hardcoded to 4
                'reservation_bank_account': 4
            }
            res = requests.post(external_bank_url+'/api/v1/transaction', data = external_bank_metadata)
            if (res.status_code == 201):
                # Make local reservation to external bank 
                sender_account = Account.objects.get(account_number=transaction.sender_account_number)
                sender_account.make_payment(transaction.amount, transaction.reservation_bank_account.account_number)
                # Update transaction status to in_progress
                transaction.status = 'in_progress'
                transaction.save()
                print(f'Reservation created for transfer with ID: {transaction.id}')
            else:
                print(f'Reservation failed for transfer with ID: {transaction.id}', res.text)