# we created this urls.py in store app in oder to separate 
#urls routs and we don't want to make it messy
from django.urls import path
#import all views from store/views.py
from . import views
urlpatterns = [
    path('search/', views.search, name = 'search'),
    path('add-to-cart/<str:product_id>/',views.add_to_cart, name = 'add_to_cart'),
    path('change-quantity/<str:product_id>/', views.change_quantity, name = 'change_quantity'),
    path('remove-from-cart/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('<slug:slug>/',views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/',views.product_detail, name='product_detail'),

    
]