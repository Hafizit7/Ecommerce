from django.urls import path
from .views import *
urlpatterns = [
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('create_bkash_payment/',create_bkash_payment, name='bkash-payment'),
    path('execute_bkash_payment/',execute_bkash_payment, name='execute_bkash_payment')
]