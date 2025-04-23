from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Аутентификация
    path('auth/login/', views.user_login, name='login'),
    path('auth/logout/', views.user_logout, name='logout'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Товары
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),

    # Категории
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),

    # Корзина
    path('cart/', views.CartItemList.as_view(), name='cart-list'),
    path('cart/<int:pk>/', views.CartItemDetail.as_view(), name='cart-detail'),

    # Заказы
    path('orders/', views.OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),

    # Избранное
    path('favorites/', views.FavoriteList.as_view(), name='favorites'),
    path('favorites/toggle/', views.toggle_favorite, name='toggle-favorite'),
]