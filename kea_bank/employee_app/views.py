from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

from account_management_app.models import Customer, Account


@login_required(login_url='login_app:login')
def index(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers,
    }

    return render(request, 'employee_app/index.html', context)


@login_required(login_url='login_app:login')
def my_profile(request):
    user = request.user
    return render(request, 'employee_app/my_profile.html', {'user': user})


@login_required(login_url='login_app:login')
def account_detail(request, account_number):
    account = Account.objects.get(account_number=account_number)
    transactions = account.get_transactions

    context = {'account': account, 'transactions': transactions}
    return render(request, 'employee_app/account_detail.html', context)


@login_required(login_url='login_app:login')
def create_customer(request):
    if (request.method == 'POST'):
        try:
            user = User.objects.create_user(
                request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'])
            customer = Customer(
                user=user,
                phone_number=request.POST['phone_number'],
                rank=request.POST['rank'],
            )
            customer.save()
            context = {
                'customer':
                customer,
                'success':
                'Customer ' + customer.user.username + ' created successfully'
            }
        except Exception:
            context = {'error': 'Error creating customer'}
            return render(request, 'employee_app/create_customer.html',
                          context)
    return render(request, 'employee_app/create_customer.html', {})


@login_required(login_url='login_app:login')
def customer_detail(request, pk):
    customer = Customer.objects.get(pk=pk)
    accounts = Account.objects.filter(user=customer.user)

    context = {
        'customer': customer,
        'accounts': accounts,
    }
    return render(request, 'employee_app/customer_detail.html', context)


@login_required(login_url='login_app:login')
def update_customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer.rank = request.POST['rank']
    customer.save()
    accounts = Account.objects.filter(user=customer.user)

    context = {
        'customer': customer,
        'accounts': accounts,
    }
    return render(request, 'employee_app/customer_detail.html', context)


@login_required(login_url='login_app:login')
def create_account(request, pk):
    if request.method == "POST":
        customer = Customer.objects.get(pk=pk)
        Account.create(user=customer.user)
        context = {'customer': customer, 'success': 'Account created'}

    else:
        context = {'error': 'Something went wrong'}
    return HttpResponseRedirect(
        reverse('employee_app:customer_detail', kwargs={'pk': pk}), context)


@login_required(login_url='login_app:login')
def delete_account(request, account_number, pk):
    if request.method == "POST":
        account = Account.objects.get(account_number=account_number)
        account.delete()
        return HttpResponseRedirect(
            reverse('employee_app:customer_detail', kwargs={'pk': pk}))
