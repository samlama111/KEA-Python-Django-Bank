from decimal import Decimal
import uuid
from django.shortcuts import render
from . models import Account, ExternalLedgerMetadata
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import chatbot

def customer_check(user):
    return hasattr(user, "customer")

@login_required(login_url='login_app:login')
@user_passes_test(customer_check, login_url='login_app:login')
def index(request):
    user = request.user
    accounts = user.customer.get_ordinary_accounts()
    total_balance = user.customer.total_balance_bank_accounts

    return render(request, 'account_management_app/index.html', {
        'accounts': accounts,
        'customer': user,
        'total_balance': total_balance
    })


def make_loan(request, account_number, pay_back=False):
    customer = request.user.customer
    my_account = Account.objects.get(account_number=account_number)
    amount_owed = my_account.get_amount_owed()
    loan_transactions = my_account.get_loan_transactions()

    if request.method == 'POST':
        if customer.rank == "basic":
            print('Cant apply for loan. Please upgrade your user rank.')
        amount = Decimal(request.POST['amount'])
        external_banks = request.user.customer.get_external_banks()
        # gets banks operational account
        our_account = customer.get_bank_operational_account()
        if pay_back:
            my_account.pay_back_loan(amount_owed, amount, our_account.account_number)
        else:
            our_account.make_payment(amount, account_number, is_loan=True)
        # gets transactions after making payment
        transactions = my_account.get_transactions()
        return render(request, 'account_management_app/account_details.html', {
            'account': my_account,
            'transactions': transactions,
            'amount_owed': amount_owed,
            'loan_transactions': loan_transactions,
            'external_banks': external_banks
        })
    else:
        return render(request, 'account_management_app/loan.html', {
            'account_number': account_number,
            'customer': customer,
            'amount_owed': amount_owed,
            'loan_transactions': loan_transactions
        })
    

@login_required(login_url='login_app:login')
@user_passes_test(customer_check, login_url='login_app:login')
def loan(request, account_number):
    return make_loan(request, account_number=account_number)

@login_required(login_url='login_app:login')
@user_passes_test(customer_check, login_url='login_app:login')
def pay_back_loan(request, account_number):
    return make_loan(request, account_number=account_number, pay_back=True)

@login_required(login_url='login_app:login')
@user_passes_test(customer_check, login_url='login_app:login')
def transfer(request, account_number):
    customer = request.user.customer
    my_account = Account.objects.get(account_number=account_number)
    accounts = customer.get_ordinary_accounts()

    context = {
        'accounts': accounts,
        'total_balance': customer.total_balance
    }
    try:
        my_account.make_payment(Decimal(request.POST['amount']), request.POST['account_number'])
        context['total_balance'] = customer.total_balance
    except Exception as e:
        context['error'] = f'There was an error: {e}'

    return render(request, 'account_management_app/index.html', context)

@login_required(login_url='login_app:login')
def account_details(request, account_number):
    account = Account.objects.get(account_number = account_number)
    transactions = account.get_transactions()
    external_banks = request.user.customer.get_external_banks()

    return render(request, 'account_management_app/account_details.html', {
        'account': account,
        'transactions': transactions,
        'external_banks': external_banks
    })


@login_required(login_url='/accounts/login/')
@user_passes_test(customer_check, login_url='login_app:login')
def my_profile(request):
    user = request.user
    return render(request, 'account_management_app/my_profile.html', {
        'customer': user.customer,
        'user': user
    })


@login_required(login_url='/accounts/login/')
@user_passes_test(customer_check, login_url='login_app:login')
def my_savings(request):
    user = request.user
    total_balance = user.customer.total_balance_saving_accounts
    accounts = Account.objects.filter(user=user, is_saving_account=True)

    return render(request, 'account_management_app/my_savings.html', {
        'accounts': accounts,
        'total_balance': total_balance
    })

@login_required(login_url='/accounts/login/')
@user_passes_test(customer_check, login_url='login_app:login')
def create_saving_account(request):
    Account.create(user=request.user, is_saving_account=True)
    return HttpResponseRedirect(reverse('account_management_app:my_savings'))

@login_required(login_url='/accounts/login/')
@user_passes_test(customer_check, login_url='login_app:login')
def saving_account_detail(request, account_number):
    account = Account.objects.get(account_number = account_number, is_saving_account=True)
    all_accounts = Account.objects.filter(user=request.user, is_saving_account=False)

    return render(request, 'account_management_app/saving_account_detail.html', {
        'account': account,
        'all_accounts': all_accounts
    })

@login_required(login_url='/accounts/login/')
@user_passes_test(customer_check, login_url='login_app:login')
def delete_saving_account(request, account_number):
    if request.method == "POST":
        account = Account.objects.get(account_number = account_number)
        account.delete()
        return HttpResponseRedirect(reverse('account_management_app:my_savings'))

@login_required(login_url='/accounts/login/')
@user_passes_test(customer_check, login_url='login_app:login')
def saving_account_transfer(request, account_number):
    customer = request.user.customer
    saving_account= Account.objects.get(account_number=account_number, is_saving_account=True)
    context={}
    if request.method == 'POST':
        transfer_account_number = request.POST.get('accounts')
        if transfer_account_number:
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
            message = 'Amount was successfully transferred to saving account'
        except Exception as ex:
            message = 'Error occurred, balance is too low'

        transactions = saving_account.get_transactions()
        context = {
            'account': saving_account,
            'transactions': transactions,
            'customer': customer,
            'message': message,
            'all_accounts': all_accounts
        }
    return render(request, 'account_management_app/saving_account_detail.html', context)

@login_required(login_url='login_app:login')
@user_passes_test(customer_check, login_url='login_app:login')
def chatbot_messages(request):
    user = request.user
    conversation = chatbot.get_conversation(user)
    context = {
        'conversation': conversation
    }
    return render(request, 'account_management_app/chatbot.html', context)

@login_required(login_url='login_app:login')
@user_passes_test(customer_check, login_url='login_app:login')
def chatbot_conversation(request):
    user = request.user

    context={}
    if (request.method == 'POST'):
        message = request.POST['message']
        response = chatbot.get_chatbot_response(message)
        conversation = chatbot.get_conversation(user)

        context = {
        'message' : message,
        'response':response,
        'conversation': conversation
        }
    return render(request, 'account_management_app/chatbot.html', context)

def external_transfer(request, account_number):
    customer = request.user.customer
    accounts = customer.get_ordinary_accounts()
    
    context = {
        'accounts': accounts,
        'total_balance': customer.total_balance_bank_accounts
    }
    
    if request.method == 'POST':
        try:
            external_bank_account = Account.objects.get(bank=request.POST['bank_id'])
            amount = Decimal(request.POST['amount'])
            external_bank_account.validate_payment(amount=amount, balance=customer.total_balance_bank_accounts)
            ExternalLedgerMetadata.objects.create(
                status='pending', token= uuid.uuid4(), reservation_bank_account=external_bank_account,
                amount=amount, sender_account_number=account_number,
                receiver_account_number=request.POST['account_number']
            )
        except Exception as e:
            context['error'] = f'There was an error: {e}'   

    return render(request, 'account_management_app/index.html', context)