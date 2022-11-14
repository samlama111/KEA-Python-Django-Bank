from django.urls import path
from . import views

app_name = 'account_management_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('transfer/<int:account_number>/', views.transfer, name="transfer"),
    path('my-profile/', views.my_profile, name="my_profile"),
    path('account_details/<int:account_number>/', views.account_details, name="account_details"),
    path('loan/<int:account_number>/', views.loan, name="loan"),
    path('loan/<int:account_number>/pay/', views.pay_back_loan, name="pay_back_loan"),
]