from django.contrib import admin
from .models import Account, Customer, Ledger, Bank, ExternalLedgerMetadata

class LedgerAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'transaction_id', 'account', )

# Register your models here.
admin.site.register(Account)
admin.site.register(Customer)
admin.site.register(Bank)
admin.site.register(ExternalLedgerMetadata)
admin.site.register(Ledger, LedgerAdmin)