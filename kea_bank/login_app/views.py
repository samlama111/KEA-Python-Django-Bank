from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http import HttpResponseRedirect


def login(request):
   context = {}

   if request.method == "POST":
      user = authenticate(request, username=request.POST['user'], password=request.POST['password'])    
      username=request.POST['user']              
      if user:
         if username =='employee':
            dj_login(request, user)
            return HttpResponseRedirect(reverse('employee_app:index'))
         else:
            dj_login(request, user)
            return HttpResponseRedirect(reverse('account_management_app:index'))
      else:
            context = {
               'error': 'Bad username or password.'
            }
   return render(request, 'login_app/login.html', context)


def logout(request):
   dj_logout(request)
   return render(request, 'login_app/login.html')


def password_reset(request):
   pass


def delete_account(request):
   pass