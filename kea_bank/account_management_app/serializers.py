from rest_framework import serializers
from .models import ExternalLedgerMetadata


class MetadataSerializer(serializers.ModelSerializer):
   class Meta:
      fields = ('token', 'reservation_bank_account', 'sender_account_number', 'receiver_account_number', 'amount')
      model = ExternalLedgerMetadata

class UpdateStateSerializer(serializers.ModelSerializer):
   class Meta:
      fields = ('status', 'id')
      model = ExternalLedgerMetadata