from rest_framework import generics

from .serializers import MetadataSerializer, UpdateStateSerializer
from .models import ExternalLedgerMetadata

class Reserve(generics.CreateAPIView):
    queryset = ExternalLedgerMetadata.objects.all()
    serializer_class = MetadataSerializer
    
class UpdateState(generics.UpdateAPIView):
    queryset = ExternalLedgerMetadata.objects.all()
    serializer_class = UpdateStateSerializer
    lookup_field = "token"