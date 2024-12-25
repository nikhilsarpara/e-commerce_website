from django.urls import path
from account.views import *


urlpatterns=[
    path('register',register,name='register'),
    path('login',login_view,name='login'),

]