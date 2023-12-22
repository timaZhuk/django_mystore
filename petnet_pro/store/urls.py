# we created this urls.py in store app in oder to separate 
#urls routs and we don't want to make it messy
from django.urls import path
#import all views from store/views.py
from . import views
urlpatterns = [
    path('search/',views.search,name='search'),
    path('<slug:slug>/',views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/',views.product_detail, name='product_detail')
]