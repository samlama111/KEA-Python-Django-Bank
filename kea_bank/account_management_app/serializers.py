from rest_framework import serializers
from .models import ExternalLedgerMetadata


class MetadataSerializer(serializers.ModelSerializer):
   class Meta:
      fields = ('sender_account', 'receiver_account', 'amount')
      model = ExternalLedgerMetadata
