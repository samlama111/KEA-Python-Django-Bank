from django.core.management.base import BaseCommand
from account_management_app.models import ExternalLedgerMetadata

import kronos
import requests


@kronos.register('* * * * *')
class Command(BaseCommand):

    def abort(self, transaction):
        print(f'Transaction with ID: {transaction.token} failed')

        url = transaction.reservation_bank_account.bank.api_url
        # send cancel request to bank
        res = requests.put(url, data={'status': 'to_be_deleted'})

        if (res.ok):
            transaction.status = 'to_be_deleted'
            transaction.save()

            print(f'Transaction with ID: {transaction.token} reverted')
        else:
            print(
                f'Transaction with ID: {transaction.token} can not be reverted, trying again'
            )

    def confirm(self, transaction):
        transaction.status = 'confirmed'
        transaction.save()
        print(
            f'Transaction reservation completed for transfer with ID: {transaction.token}'
        )

    def handle(self, *args, **options):
        # Get all pending transactions in External Ledger Table
        pending_transactions = ExternalLedgerMetadata.objects.filter(
            status='pending')

        # Make POST request to bank API to create a reservation
        for transaction in pending_transactions:
            if transaction.failed_attempts > 2:
                self.abort(transaction)
                break

            if transaction.successful_attempts > 2:
                self.confirm(transaction)
                break

            print(
                f'Creating reservation for transfer with ID: {transaction.token}'
            )
            external_bank_url = transaction.reservation_bank_account.bank.api_url
            external_bank_metadata = {
                'amount': int(transaction.amount
                              ),  # int as Decimal can't be sent in JSON
                'receiver_account_number': transaction.receiver_account_number,
                'sender_account_number': transaction.sender_account_number,
                # TODO: Local bank's ID in external bank is hardcoded to 4
                'reservation_bank_account': 4,
                'token': transaction.token,
                'status': 'in_progress',
            }
            try:
                res = requests.post(external_bank_url + '/api/v1/transaction',
                                    data=external_bank_metadata)
                if (res.status_code == 201):
                    print(
                        f'Reservation created for transfer with ID: {transaction.token}'
                    )

                    url = external_bank_url + f'/api/v1/transaction/{transaction.token}/'

                    for i in range(3):
                        res = requests.put(url,
                                           data={'status': 'to_be_confirmed'})
                        if res.ok:
                            transaction.successful_attempts += 1
                        else:
                            transaction.failed_attempts += 1
                        transaction.save()
                else:
                    transaction.failed_attempts += 1
                    transaction.save()
                    print(
                        f'Reservation failed for transfer with ID: {transaction.token}',
                        res.text)
            except Exception:
                transaction.failed_attempts += 1
                transaction.save()
                print(
                    f'Reservation failed for transfer with ID: {transaction.token}'
                )
