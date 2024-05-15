from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category_page'),
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('register/', user_register_view, name='register'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product'),
    path('product_by_color/<str:model_product>/<str:color_code>/', get_product_by_color, name='product_color'),
    path('save_favorite/<slug:slug>/', save_favorite_product, name='save_favorite'),
    path('favorite/', FavoriteProductView.as_view(), name='favorite'),
    path('to_cart/<slug:slug>/<str:action>/', to_cart_view, name='to_cart'),
    path('my_cart/', my_cart_view, name='my_cart'),
    path('checkout', checkout_view, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment, name='success'),
    path('profile/<int:pk>', profile_view, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),


]