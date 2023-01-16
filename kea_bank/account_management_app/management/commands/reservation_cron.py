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
            print(f'Creating reservation for transfer with ID: {transaction.token}')
            external_bank_url = transaction.reservation_bank_account.bank.api_url
            external_bank_metadata = {
                'amount': int(transaction.amount),
                'receiver_account_number': transaction.receiver_account_number, 
                'sender_account_number': transaction.sender_account_number,
                # Local bank's ID in external bank is hardcoded to 4
                'reservation_bank_account': 4,
                'token': transaction.token,
                'status': 'in_progress',
            }
            res = requests.post(external_bank_url+'/api/v1/transaction', data = external_bank_metadata)
            if (res.status_code == 201):
                print(f'Reservation created for transfer with ID: {transaction.token}')

                url = external_bank_url+f'/api/v1/transaction/{transaction.token}/'

                # TODO: repeat n times
                res = requests.put(url, data = {'status': 'to_be_confirmed' })

                if res.ok:
                    transaction.status = 'confirmed'
                    transaction.save()
                    print(f'Transaction completed for transfer with ID: {transaction.token}')
                else:
                    print(f'Transaction with ID: {transaction.token} failed', res.text)
                    transaction.reservation_bank_account.make_payment(transaction.amount, transaction.sender_account_number, is_loan=True)
                    
                    transaction.status = 'to_be_deleted'
                    transaction.save()
                    
                    # send cancel request to bank
                    requests.put(url, data = {'status': 'to_be_deleted' })

                    print(f'Transaction with ID: {transaction.token} reverted')
            else:
                print(f'Reservation failed for transfer with ID: {transaction.token}', res.text)