from django.urls import path 
from .views import *
urlpatterns = [
    path('dashboard/home', dashboard, name='dashboard'),
    path('dashboard/banner-list', banner_list, name= 'banner-list'),
]