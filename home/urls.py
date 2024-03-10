from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('delete/', delete_address),
    path('update/', update_address)
]
