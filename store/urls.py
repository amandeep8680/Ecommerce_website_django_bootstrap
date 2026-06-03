from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path(
        'products/',
        views.products,
        name='products'
    ),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'category/<int:category_id>/',
        views.category_products,
        name='category_products'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'add-to-cart/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

   path(
    'logout/',
    auth_views.LogoutView.as_view(
        next_page='login'
    ),
    name='logout'
),

path(
    'wishlist/',
    views.wishlist,
    name='wishlist'
),

path(
    'add-to-wishlist/<int:product_id>/',
    views.add_to_wishlist,
    name='add_to_wishlist'
),

path(
    'remove-wishlist/<int:wishlist_id>/',
    views.remove_wishlist,
    name='remove_wishlist'
),

path(
    'add-review/<int:product_id>/',
    views.add_review,
    name='add_review'
),

path(
    'profile/',
    views.profile,
    name='profile'
),

path(
    'order-success/',
    views.order_success,
    name='order_success'
),

path(
    'increase-cart/<int:product_id>/',
    views.increase_cart,
    name='increase_cart'
),

path(
    'decrease-cart/<int:product_id>/',
    views.decrease_cart,
    name='decrease_cart'
),

path(
    'remove-cart/<int:product_id>/',
    views.remove_cart,
    name='remove_cart'
),




]
