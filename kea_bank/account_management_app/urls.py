from django.urls import path
from . import views
from .api import Reserve, UpdateState

app_name = 'account_management_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('transfer/<int:account_number>/', views.transfer, name="transfer"),
    path('my-profile/', views.my_profile, name="my_profile"),
    path('chatbot/', views.chatbot_messages, name="chatbot_messages"),
    path('message/', views.chatbot_conversation, name = "chatbot_conversation" ),
    path('account_details/<int:account_number>/', views.account_details, name="account_details"),
    path('loan/<int:account_number>/', views.loan, name="loan"),
    path('loan/<int:account_number>/pay/', views.pay_back_loan, name="pay_back_loan"),
    path('my_savings/', views.my_savings, name="my_savings"),
    path('create-saving-account/', views.create_saving_account, name="create_saving_account"),
    path('saving-account-detail/<int:account_number>/', views.saving_account_detail, name="saving_account_detail"),
    path('delete-account/<int:account_number>', views.delete_saving_account, name="delete_saving_account"),
    path('saving_account_transfer/<int:account_number>/', views.saving_account_transfer, name="saving_account_transfer"),
    path('api/v1/transaction', Reserve.as_view()), #post
    path('api/v1/transaction/<uuid:token>/', UpdateState.as_view()), #put
]