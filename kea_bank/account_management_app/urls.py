from django.urls import path
from . import views

app_name = 'account_management_app'

urlpatterns = [
    path('index', views.index, name="index"),
    path('my-profile', views.index, name="my_profile")

]