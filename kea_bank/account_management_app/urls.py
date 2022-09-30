from django.urls import path
from . import views

app_name = 'account_management_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('transfer/<int:account_number>/', views.transfer, name="transfer"),
    path('my-profile/<int:customer_id>/', views.my_profile, name="my_profile"),
    path('account_details/<int:account_number>/', views.account_details, name="account_details"),
    path('loan/<int:account_number>/<int:customer_id>/', views.loan, name="loan"),
]