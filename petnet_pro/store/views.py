from django.db.models import Q # for search field
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# category view
def category_detail(request, slug):
    category = get_object_or_404(Category,slug = slug)
    products = category.products.all()
    return render(request, 'store/category_detail.html',
                  {'category':category,
                   'products':products})

# Create your views here.
def product_detail(request,category_slug,slug):
    product =get_object_or_404(Product,slug = slug)
    return render(request,'store/product_detail.html',{
        'product':product
    })


# for Search field
def search(request):
    query = request.GET.get('query','') # get data from search fiels with name query
    products = Product.objects.filter(Q(title__icontains=query)&
                                      Q(description__icontains=query))
    return render(request, 'store/search.html',{
        'query':query,
        'products':products
    })

