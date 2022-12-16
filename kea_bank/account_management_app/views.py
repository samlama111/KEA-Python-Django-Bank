from decimal import Decimal
from django.shortcuts import render
from django.http import Http404
from . models import Account
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import chatbot

from . models import Customer

@login_required(login_url='login_app:login')
def index(request):
    try:
        user = request.user
        accounts = Account.objects.filter(user=user, is_saving_account=False)
        total_balance = user.customer.total_balance_bank_accounts

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


@login_required(login_url='/accounts/login/')
def my_savings(request):
    try:
        user = request.user
        total_balance = user.customer.total_balance_saving_accounts
        accounts = Account.objects.filter(user=user, is_saving_account=True)

        return render(request, 'account_management_app/my_savings.html', {
            'accounts': accounts,
            'total_balance': total_balance
        })
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )

@login_required(login_url='/accounts/login/')
def create_saving_account(request):
    try:
        user = request.user
        saving_account = Account(user=user, is_saving_account=True)
        saving_account.save()
        return HttpResponseRedirect(reverse('account_management_app:my_savings'))
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )

@login_required(login_url='/accounts/login/')
def saving_account_detail(request, account_number):
    try:
        account = Account.objects.get(account_number = account_number, is_saving_account=True)
        all_accounts = Account.objects.filter(user=request.user, is_saving_account=False)

        return render(request, 'account_management_app/saving_account_detail.html', {
            'account': account,
            'all_accounts': all_accounts
        })
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )

@login_required(login_url='/accounts/login/')
def delete_saving_account(request, account_number):
    try:

         if request.method == "POST":
            account = Account.objects.get(account_number = account_number)
            account.delete()
            return HttpResponseRedirect(reverse('account_management_app:my_savings'))
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )

@login_required(login_url='/accounts/login/')
def saving_account_transfer(request, account_number):
    try:
        customer = request.user.customer
        saving_account= Account.objects.get(account_number=account_number, is_saving_account=True)
        print(type(saving_account))
        if request.method == 'POST':
            if request.POST.get('accounts') and request.POST.get('accounts'):
                transfer_account_number = request.POST.get('accounts')
                amount = Decimal(request.POST['amount'])
            else:
                return render(request, 'account_management_app/saving_account_detail.html', {
                    'account': saving_account,
                    'message': 'Please select an amount and account to transfer to'
                })
            transfer_account = Account.objects.get(account_number=transfer_account_number)
            all_accounts = Account.objects.filter(user=request.user, is_saving_account=False)

            try:
                transfer_account.make_payment(amount, saving_account.account_number, is_loan=False, is_saving_account=True)
                message = 'Amount was sucessfully transfered to saving account'
            except Exception as ex:
                message = 'Error occured, balance is too low'

            transactions = saving_account.get_transactions
            context = {
                'account': saving_account,
                'transactions': transactions,
                'customer': customer,
                'message': message,
                'all_accounts': all_accounts

            }
            return render(request, 'account_management_app/saving_account_detail.html', context)
        else:
            return render(request, 'account_management_app/saving_account_detail.html', context)
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )

@login_required(login_url='login_app:login')
def chatbot_messages(request):
    try:
        context = {}
        return render(request, 'account_management_app/chatbot.html', context)
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )

@login_required(login_url='login_app:login')
def chatbot_conversation(request):
    try:
        if (request.method == 'POST'):
            message = request.POST['message']
            response = chatbot.get_chatbot_response(message)
            conversation = chatbot.get_conversation()

            context = {
            'message' : message,
            'response':response,
            'conversation': conversation
            }
            return render(request, 'account_management_app/chatbot.html', context)
        else:
            context = {}
            return render(request, 'account_management_app/chatbot.html', context)
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )