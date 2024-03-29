from django.urls import path
from . import views
from .api import Reserve, GetUpdateStatus

app_name = 'account_management_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('login-success/', views.login_success, name="login_success"),
    path('transfer/<int:account_number>/', views.transfer, name="transfer"),
    path('transfer/external/<int:account_number>/',
         views.external_transfer,
         name="external_transfer"),
    path('my-profile/', views.my_profile, name="my_profile"),
    path('chatbot/', views.chatbot_conv, name="chatbot_conv"),
    path('message/', views.chatbot_messages, name="chatbot_messages"),
    path('account-details/<int:account_number>/',
         views.account_details,
         name="account_details"),
    path('loan/<int:account_number>/', views.loan, name="loan"),
    path('loan/<int:account_number>/pay/',
         views.pay_back_loan,
         name="pay_back_loan"),
    path('my-savings/', views.my_savings, name="my_savings"),
    path('create-saving-account/',
         views.create_saving_account,
         name="create_saving_account"),
    path('saving-account-detail/<int:account_number>/',
         views.saving_account_detail,
         name="saving_account_detail"),
    path('delete-account/<int:account_number>',
         views.delete_saving_account,
         name="delete_saving_account"),
    path('saving-account-transfer/<int:account_number>/',
         views.saving_account_transfer,
         name="saving_account_transfer"),
    path('api/v1/transaction', Reserve.as_view()),  # post
    path('api/v1/transaction/<uuid:token>/',
         GetUpdateStatus.as_view()),  # get, put
]
