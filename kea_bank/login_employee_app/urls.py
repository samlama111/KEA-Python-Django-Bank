from django.urls import path
from . import views


app_name = 'login_employee_app'

urlpatterns = [
   path('employee-login/', views.employee_login, name='employee_login'),
   path('logout/', views.logout, name='logout'),
   path('employee-password_reset/', views.password_reset, name='password_reset'),
   path('employee-sign-up/', views.employee_sign_up, name='employee_sign_up'),
   path('employee-delete_account/', views.password_reset, name='password_reset'),
]