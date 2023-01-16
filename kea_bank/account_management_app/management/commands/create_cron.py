from django.core.management.base import BaseCommand
from account_management_app.models import ExternalLedgerMetadata, Account

import requests
import kronos

@kronos.register('* * * * *')
class Command(BaseCommand):
    def abort(self, transaction):
        print(f'Receiver does not exist, cancelling transaction with ID: {transaction.token}')
        # Abort locally
        transaction.status = 'cancelled'
        transaction.save()

        # And abort transaction by calling update state to cancel
        external_bank_url = transaction.reservation_bank_account.bank.api_url
        url = external_bank_url+f'/api/v1/transaction/{transaction.token}/'
        # From receiver to reservation
        requests.put(url, data = {'status': 'to_be_deleted' })
    
    def handle(self, *args, **options):
        to_be_created_transactions = ExternalLedgerMetadata.objects.filter(status='to_be_confirmed')
        
        for transaction in to_be_created_transactions:
            # If receiver doesn't exist, cancel locally
            try:
                receiver_account = Account.objects.get(account_number=transaction.receiver_account_number)
                if receiver_account:
                    external_bank_url = transaction.reservation_bank_account.bank.api_url
                    url = external_bank_url+f'/api/v1/transaction/{transaction.token}/'
                    # TODO: repeat
                    transaction_status = requests.get(url)
                    if transaction_status.json()['status'] == 'confirmed':
                        # TODO: change to successful attempts
                        # Create entry in local ledger
                        transaction.reservation_bank_account.make_payment(transaction.amount, transaction.receiver_account_number, is_loan=True)
                        # Update status to confirmed
                        transaction.status = 'confirmed'
                        transaction.save()
                        print(f'Transaction finished for transfer with ID: {transaction.token}')
                    else: 
                        # TODO: change to unsuccessful attempts
                        self.abort(transaction)
                else: 
                    self.abort(transaction)
            except Exception:
                self.abort(transaction)
            