from django.core.management.base import BaseCommand
from account_management_app.models import ExternalLedgerMetadata

import requests
import kronos

@kronos.register('* * * * *')
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Get all in progress transactions in External Ledger Table
        in_progress_transactions = ExternalLedgerMetadata.objects.filter(status='in_progress')
        
        for transaction in in_progress_transactions:
            # For now, confirm just once
            no_of_tries = 5
            min_successful_tries = 3
            
            print(f'Confirming transaction with ID: {transaction.token}')
            external_bank_url = transaction.reservation_bank_account.bank.api_url
            url = external_bank_url+f'/api/v1/transaction/{transaction.token}/'

            res = requests.put(url, data = {'status': 'to_be_confirmed' })

            print(res.status_code)
            if res.ok:
                transaction.status = 'confirmed'
                transaction.save()
                print(f'Transaction completed for transfer with ID: {transaction.token}')
            else:
                print(f'Transaction with ID: {transaction.token} failed', res.text)
                # set status to cancelled, 
                transaction.status = 'cancelled'
                transaction.save()
                
                # negate reservation transaction in Ledger table
                transaction.reservation_bank_account.make_payment(transaction.amount, transaction.sender_account_number)
                
                # send cancel request to bank
                res = requests.put(url, data = {'status': 'cancelled' })

                print(f'Transaction with ID: {transaction.token} reverted')

            # if (transaction.tried < no_of_tries):
                # increment tried by one
            # else: 