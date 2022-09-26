from django.shortcuts import render

def index(request):
    return render(request, 'account_management_app/index.html', {})