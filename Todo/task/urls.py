from django.urls import path
from .views import  *


app_name = 'task'

urlpatterns = [
    path('' , Home , name = 'Home'),
    path('remove_task/' , remove_task , name = 'remove_task'),
    path('create_task/' , create_task , name = 'create_task'),
    path('done/' , done ,name = 'done'),
]