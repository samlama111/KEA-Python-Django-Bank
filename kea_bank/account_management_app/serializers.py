from rest_framework import serializers
from .models import ExternalLedgerMetadata


class MetadataSerializer(serializers.ModelSerializer):
   class Meta:
      fields = ('reservation_bank_account', 'sender_account_number', 'receiver_account_number', 'amount')
      model = ExternalLedgerMetadata
