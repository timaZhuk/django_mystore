from django.shortcuts import render

#import model Products
from store.models import Product
# Create your views here.
# Then we have to add this view to main url.py inside petnet_pro



#1 view for frontpage
def frontpage(request):
    products = Product.objects.all()[0:6] # show only first six items

    return render(request, 'core/frontpage.html', {
        'products':products
    })

#2 view for about
def about(request):
    return render(request,'core/about.html') 