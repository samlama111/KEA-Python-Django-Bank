from django.urls import path
from . import views

app_name = 'account_management_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('transfer/', views.transfer, name="transfer"),
    path('my-profile/', views.index, name="my_profile"),
    path('account_details/<int:account_number>/', views.account_details, name="account_details")
]