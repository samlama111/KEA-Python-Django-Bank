from django.shortcuts import render
from . models import Account

def index(request):
    accounts = Account.objects.all()
    return render(request, 'account_management_app/index.html', {
        'accounts': accounts,
        'test_account': accounts[0]
    })

def transfer(request):
    account_number = request.POST['my_account_number']     
    my_account = Account.objects.get(account_number=account_number)
   
    my_account.make_payment(request.POST['amount'], request.POST['account_number'])
    accounts = Account.objects.all()
    return render(request, 'account_management_app/index.html', {
        'accounts': accounts,
        'test_account': accounts[0]
    })

def my_profile(request):
    return render(request, 'account_management_app/my_profile.html', {})