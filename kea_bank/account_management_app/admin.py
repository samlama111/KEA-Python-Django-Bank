from django.contrib import admin
from .models import Account, Customer, Ledger

# Register your models here.
admin.site.register(Account)
admin.site.register(Customer)
admin.site.register(Ledger)