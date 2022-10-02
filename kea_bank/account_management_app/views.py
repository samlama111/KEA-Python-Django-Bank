from django.shortcuts import render
from . models import Account, Customer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


@login_required(login_url='login_app:login')
def index(request):
    customer = request.user.customer
    accounts = Account.objects.filter(customer=customer)
    total_balance = customer.total_balance

    return render(request, 'account_management_app/index.html', {
        'accounts': accounts,
        'customer': request.user,
        'total_balance': total_balance
    })

@login_required(login_url='login_app:login')
def loan(request, account_number, customer_id):
    customer = request.user.customer

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
            'account_number': account_number,
            'customer': customer
        })

@login_required(login_url='login_app:login')
def transfer(request, account_number):
    customer = request.user.customer
    my_account = Account.objects.get(account_number=account_number)
    accounts = Account.objects.filter(customer=request.user.customer)
   
    try:
        my_account.make_payment(request.POST['amount'], request.POST['account_number'])
        context = {
            'accounts': accounts,
            'total_balance': customer.total_balance
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

@login_required(login_url='login_app:login')
def account_details(request, account_number):
    account = Account.objects.get(account_number = account_number)
    customer = request.user

    return render(request, 'account_management_app/account_details.html', {
        'account': account,
        'customer':customer
    })

@login_required(login_url='/accounts/login/')
def my_profile(request):
    customer = request.user.customer
    return render(request, 'account_management_app/my_profile.html', {
        'customer': customer
    })