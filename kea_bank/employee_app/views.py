from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView,ListView, DetailView, UpdateView

from . models import Employee

def index(request):
    return render(request, 'employee_app/index.html', {})

def all_customers(request):
    return render(request, 'employee_app/index.html', {})


def my_profile(request):
    return render(request, 'employee_app/index.html', {})


def account_details(request):
    return render(request, 'employee_app/index.html', {})


def create_customer(request):
    return render(request, 'employee_app/index.html', {})
