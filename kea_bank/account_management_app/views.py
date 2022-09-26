from django.shortcuts import render
from . models import Account
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    accounts = Account.objects.all()
    return render(request, 'account_management_app/index.html', {
        'accounts': accounts,
    })

def transfer(request):
    account_number = request.POST['my_account_number']     
    my_account = Account.objects.get(account_number=account_number)
    accounts = Account.objects.all()
   
    try:
        my_account.make_payment(request.POST['amount'], request.POST['account_number'])
        context = {
            'accounts': accounts,
            'test_account': accounts[0]
        }
    except ObjectDoesNotExist as objectError:
        context = { 
            'accounts': accounts,
            'error': f'there was an error: {objectError}'
        }
    except Exception as e:
        context = { 
            'accounts': accounts,
            'error': f'there was an error: {e.message}'
        }
    return render(request, 'account_management_app/index.html', context)

def account_details(request, account_number):
    accounts = Account.objects.get(account_number = account_number)
    return render(request, 'account_management_app/account_details.html', {
        'accounts': accounts,
        'test_account': accounts
    })



def my_profile(request):
    return render(request, 'account_management_app/my_profile.html', {})