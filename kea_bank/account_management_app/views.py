from decimal import Decimal
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

def make_loan(request, account_number, pay_back=False):
    customer = request.user.customer
    my_account = Account.objects.get(account_number=account_number)
    amount_owed = my_account.get_amount_owed()
    loan_transactions = my_account.get_loan_transactions()

    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        # TODO: replace 9999 with the bank's account number
        our_account = Account.objects.get(account_number=9999)
        if pay_back:
            if amount_owed >= amount:
                my_account.make_payment(amount, our_account.account_number, is_loan=True)
            else:
                # TODO: display error message
                print('Cant return more than what you owe')
        else:
            our_account.make_payment(amount, account_number, is_loan=True)
        transactions = my_account.get_transactions
        return render(request, 'account_management_app/account_details.html', {
            'account': my_account,
            'transactions': transactions,
            'amount_owed': amount_owed,
            'loan_transactions': loan_transactions
        })
    else:
        return render(request, 'account_management_app/loan.html', {
            'account_number': account_number,
            'customer': customer,
            'amount_owed': amount_owed,
            'loan_transactions': loan_transactions
        })

@login_required(login_url='login_app:login')
def loan(request, account_number):
    return make_loan(request, account_number=account_number)

@login_required(login_url='login_app:login')
def pay_back_loan(request, account_number):
    return make_loan(request, account_number=account_number, pay_back=True)

@login_required(login_url='login_app:login')
def transfer(request, account_number):
    customer = request.user.customer
    my_account = Account.objects.get(account_number=account_number)
    accounts = Account.objects.filter(customer=request.user.customer)
   
    context = {
        'accounts': accounts,
        'total_balance': customer.total_balance
    }
    try:
        my_account.make_payment(Decimal(request.POST['amount']), request.POST['account_number'])
    except Exception as e:
        context['error'] = f'there was an error: {e}'

    return render(request, 'account_management_app/index.html', context)

@login_required(login_url='login_app:login')
def account_details(request, account_number):
    account = Account.objects.get(account_number = account_number)
    transactions = account.get_transactions

    return render(request, 'account_management_app/account_details.html', {
        'account': account,
        'transactions': transactions
    })

@login_required(login_url='/accounts/login/')
def my_profile(request):
    customer = request.user.customer
    return render(request, 'account_management_app/my_profile.html', {
        'customer': customer
    })