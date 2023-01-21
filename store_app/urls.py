from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('product_detail/<pk>', product_detail, name='product-detail'),
    path('about-abc', aboutus, name='about-page'),
    path('product_search', product_search, name='product-search'),
    path('product-category/<pk>', category_filtering, name = 'category-product'),
    path('add-to-cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('remove-cart/<pk>/', remove_cart, name='remove-cart'),
    path('cart-summary', cart_summary, name='cart-summary'),
    path('cart-increment/<pk>/', cart_increment, name='cart-increment'),
    path('cart-decrement/<pk>/', cart_decrement, name='cart-decrement'),
    path('order-history/', order_summary, name='order-history'),
    path('order/details/<pk>', OrderDetails, name='order-details'),
    path('add-to-wishlist/<pk>/', add_to_wishlist, name='add-to-wishlist'),
    path('ordered/product/review/<int:pk>/', review, name='order-item-review'),
]