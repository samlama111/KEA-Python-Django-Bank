from decimal import Decimal
from django.shortcuts import render
from django.http import Http404
from . models import Account
from django.contrib.auth.decorators import login_required

from . models import Customer
@login_required(login_url='login_app:login')
def index(request):
    try:
        user = request.user
        accounts = Account.objects.filter(user=user)
        total_balance = user.customer.total_balance

        return render(request, 'account_management_app/index.html', {
            'accounts': accounts,
            'customer': user,
            'total_balance': total_balance
        })
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )


def make_loan(request, account_number, pay_back=False):
    try:
        customer = request.user.customer
        my_account = Account.objects.get(account_number=account_number)
        amount_owed = my_account.get_amount_owed()
        loan_transactions = my_account.get_loan_transactions()

        if request.method == 'POST':
            if customer.rank == "basic":
                print('Cant apply for loan. Please upgrade your user rank.')
            amount = Decimal(request.POST['amount'])
            # gets banks operational account
            our_account = Account.objects.filter(is_customer=False)[0]
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
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )
    

@login_required(login_url='login_app:login')
def loan(request, account_number):
    try:
        return make_loan(request, account_number=account_number)
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )

@login_required(login_url='login_app:login')
def pay_back_loan(request, account_number):
    try:
        return make_loan(request, account_number=account_number, pay_back=True)

    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )

@login_required(login_url='login_app:login')
def transfer(request, account_number):
    try:
        customer = request.user.customer
        my_account = Account.objects.get(account_number=account_number)
        accounts = Account.objects.filter(user=request.user)
    
        try:
            my_account.make_payment(Decimal(request.POST['amount']), request.POST['account_number'])
        except Exception as e:
            context['error'] = f'there was an error: {e}'

        context = {
            'accounts': accounts,
            'total_balance': customer.total_balance
        }
        return render(request, 'account_management_app/index.html', context)
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )


@login_required(login_url='login_app:login')
def account_details(request, account_number):
    try:
        account = Account.objects.get(account_number = account_number)
        transactions = account.get_transactions

        return render(request, 'account_management_app/account_details.html', {
            'account': account,
            'transactions': transactions
        })
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )


@login_required(login_url='/accounts/login/')
def my_profile(request):
    try:
        user = request.user
        return render(request, 'account_management_app/my_profile.html', {
            'customer': user.customer,
            'user': user
        })
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )
