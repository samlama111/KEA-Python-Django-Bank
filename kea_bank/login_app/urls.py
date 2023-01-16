from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'login_app'

urlpatterns = [
   path('login/', views.login, name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('password-reset/', views.password_reset, name='password_reset'),
   path('delete-account/', views.delete_account, name='delete_account'),
]