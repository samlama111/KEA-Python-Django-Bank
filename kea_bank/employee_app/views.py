from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView,ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required


from account_management_app.models import Customer
from account_management_app.models import Account

from . models import Employee

@login_required(login_url='login_app:login')
def index(request):
    if hasattr(request.user,'employee'):
        return render(request, 'employee_app/index.html', {})
    else:
        return render(request, 'login_app/login.html', {})

@login_required(login_url='login_app:login')
def all_customers(request):
    if hasattr(request.user,'employee'):
        customers = Customer.objects.all()
        context = {
            'customers': customers,
        }

        return render(request, 'employee_app/all_customers.html', context)
    else:
        return render(request, 'login_app/login.html', {})

@login_required(login_url='login_app:login')
def my_profile(request):
    if hasattr(request.user,'employee'):
        return render(request, 'employee_app/index.html', {})
    else:
        return render(request, 'login_app/login.html', {})

@login_required(login_url='login_app:login')
def account_detail(request, account_number):
    if hasattr(request.user,'employee'):
        try:
            account = Account.objects.get(account_number = account_number)
            transactions = account.get_transactions

            context = {
                'account': account,
                'transactions': transactions
            }
            return render(request, 'employee_app/account_detail.html', context)

        except Customer.DoesNotExist:
            raise Http404("Customer does not exist")
    else:
        return render(request, 'login_app/login.html', {})

@login_required(login_url='login_app:login')
def create_customer(request):
    if hasattr(request.user,'employee'):
        return render(request, 'employee_app/index.html', {})
    else:
        return render(request, 'login_app/login.html', {})

@login_required(login_url='login_app:login')
def customer_detail(request, pk):
    if hasattr(request.user,'employee'):
        try:
            customer = Customer.objects.get(pk = pk)
            accounts = Account.objects.filter(user=customer.user)

            context = {
                'customer': customer,
                'accounts': accounts,
            }
            return render(request, 'employee_app/customer_detail.html', context)

        except Customer.DoesNotExist:
            raise Http404("Customer does not exist")

    else:
        return render(request, 'login_app/login.html', {})