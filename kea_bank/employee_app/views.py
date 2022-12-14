from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView,ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User


from account_management_app.models import Customer
from account_management_app.models import Account
from django.shortcuts import redirect


from . models import Employee

@login_required(login_url='login_app:login')
def index(request):
    if hasattr(request.user,'employee'):
        try:
            customers = Customer.objects.all()
            context = {
                'customers': customers,
            }

            return render(request, 'employee_app/index.html', context)
        except Customer.DoesNotExist:
            return render(request, 'login_app/login.html', {})
    else:
        return render(request, 'login_app/login.html', {})



@login_required(login_url='login_app:login')
def my_profile(request):
    if hasattr(request.user,'employee'):
        try:
            return render(request, 'employee_app/index.html', {})
        except Customer.DoesNotExist:
            return render(request, 'login_app/login.html', {})
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
            return render(request, 'login_app/login.html', {})
    else:
        return render(request, 'login_app/login.html', {})

@login_required(login_url='login_app:login')
def create_customer(request):
    if hasattr(request.user,'employee'):
        if (request.method == 'POST'):
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name']
                )
                customer = Customer(
                    user=user,
                    phone_number=request.POST['phone_number'],
                    rank=request.POST['rank'],
                )
                customer.save()
                context = {
                    'customer': customer,
                    'success': 'Customer ' + customer.user.username + ' created successfully'
                }
            except:
                context = {
                    'error': 'Error creating customer'
                }
                return render(request, 'employee_app/create_customer.html', context)
            else:
                return render(request, 'employee_app/create_customer.html', context)
        return render(request, 'employee_app/create_customer.html', {})
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

@login_required(login_url='login_app:login')
def update_customer(request, pk):
    if hasattr(request.user,'employee'):
        try:
            customer = Customer.objects.get(pk = pk)
            customer.rank = request.POST['rank']
            customer.save()

            context = {
                'customer': customer,
            }
            return render(request, 'employee_app/customer_detail.html', context)

        except Customer.DoesNotExist:
            raise Http404("Customer does not exist")

    else:
        return render(request, 'login_app/login.html', {})
        
@login_required(login_url='login_app:login')
def create_account(request, pk):
    if hasattr(request.user,'employee'):
        if request.method == "POST":
            customer = Customer.objects.get(pk = pk)
            account = Account(user=customer.user)
            account.save()
            context = {
                'customer': customer,
                'success': 'Account created'
            }

        else:
            context = {
                'error': 'Something went wrong'
        }
        return HttpResponseRedirect(reverse('employee_app:customer_detail', kwargs={'pk':pk}))

@login_required(login_url='login_app:login')
def delete_account(request, account_number, pk):
    if hasattr(request.user,'employee'):
        if request.method == "POST":
            account = Account.objects.get(account_number = account_number)
            account.delete()
            return HttpResponseRedirect(reverse('employee_app:customer_detail', kwargs={'pk':pk}))
    else:
        return render(request, 'login_app/login.html', {})

@login_required(login_url='/accounts/login/')
def my_profile(request):
    try:
        user = request.user
        return render(request, 'employee_app/my_profile.html', {
            'user': user
        })
    except Customer.DoesNotExist:
        return render(request,'login_app/login.html', {} )
