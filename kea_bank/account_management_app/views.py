from django.shortcuts import render
from . models import Account
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    accounts = Account.objects.all()
    return render(request, 'account_management_app/index.html', {
        'accounts': accounts,
    })

def loan(request, account_number):
    if request.method == 'POST':
        # TODO: replace 9999 with the bank's account number
        our_account = Account.objects.get(account_number=9999)
        our_account.make_payment(request.POST['amount'], account_number)
        my_account = Account.objects.get(account_number=account_number)
        return render(request, 'account_management_app/account_details.html', {
            'account': my_account
        })
    else:
        return render(request, 'account_management_app/loan.html', {
            'account_number': account_number
        })


def transfer(request, account_number):
    my_account = Account.objects.get(account_number=account_number)
    accounts = Account.objects.all()
   
    try:
        my_account.make_payment(request.POST['amount'], request.POST['destination_account_number'])
        context = {
            'accounts': accounts
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
    account = Account.objects.get(account_number = account_number)
    return render(request, 'account_management_app/account_details.html', {
        'account': account
    })



def my_profile(request):
    return render(request, 'account_management_app/my_profile.html', {})