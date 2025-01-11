from django.urls import path
from .views import *


app_name = 'user'

urlpatterns = [
    path('' , Home , name = 'Home'),
    path('register/' , register , name = 'register'),
    path('login/' , login , name = 'login'),
    path('logout/' , logout , name = 'logout'),
    path('forgetPass/' , forgetPass , name = 'forgetPass'),
    path('verify_otp/', verify_otp ,  name = 'verify_otp'),
    path('profile_view/' , profile_view, name = 'profile_view'),
    path('get_start/' , get_start , name = 'get_start'),

]