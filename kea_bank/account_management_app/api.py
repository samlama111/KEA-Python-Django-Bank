from rest_framework import generics

from .serializers import MetadataSerializer
from .models import ExternalLedgerMetadata

class Transfer(generics.CreateAPIView):
    queryset = ExternalLedgerMetadata.objects.all()
    serializer_class = MetadataSerializer