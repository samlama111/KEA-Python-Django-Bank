from django.urls import path
from . import views
from two_factor.urls import urlpatterns as tf_urls
from django.contrib.auth.views import LogoutView


app_name = 'login_app'

urlpatterns = [
   path('login/', views.login, name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('password_reset/', views.password_reset, name='password_reset'),
   path('delete_account/', views.delete_account, name='delete_account'),

]