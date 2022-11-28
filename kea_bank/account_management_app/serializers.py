from rest_framework import serializers
from .models import ExternalLedgerMetadata


class MetadataSerializer(serializers.ModelSerializer):
   class Meta:
      fields = ('local_account', 'target_bank', 'amount')
      model = ExternalLedgerMetadata
