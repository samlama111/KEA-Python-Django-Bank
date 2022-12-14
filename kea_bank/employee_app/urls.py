from django.urls import path
from . import views

app_name = 'employee_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('customer/<int:pk>/', views.customer_detail, name="customer_detail"),
    path('update-customer/<int:pk>/', views.update_customer, name="update_customer"),
    path('my-profile/', views.my_profile, name="my_profile"),
    path('create-customer/', views.create_customer, name="create_customer"),
    path('account_detail/<int:account_number>/', views.account_detail, name="account_detail"),
    path('create-account/<int:pk>', views.create_account, name="create_account"),
    path('delete-account/<int:account_number>/<int:pk>', views.delete_account, name="delete_account")


]