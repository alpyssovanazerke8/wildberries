from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/login/', views.user_login, name='login'),
    path('auth/logout/', views.user_logout, name='logout'),

    # Products
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),

    # Categories
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),

    # Cart
    path('cart/', views.CartItemList.as_view(), name='cart-list'),
    path('cart/<int:pk>/', views.CartItemDetail.as_view(), name='cart-detail'),

    # Orders
    path('orders/', views.OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),
]