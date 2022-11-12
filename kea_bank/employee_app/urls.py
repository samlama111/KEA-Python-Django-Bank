from django.urls import path
from . import views

app_name = 'employee_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('all-customers/', views.all_customers, name="all_customers"),
    path('customer/<int:pk>/', views.customer_detail, name="customer_detail"),
    path('my-profile/', views.my_profile, name="my_profile"),
    path('create-customer/', views.create_customer, name="create_customer"),
    path('account_details/<int:account_number>/', views.account_details, name="account_details"),
]