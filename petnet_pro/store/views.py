from django.db.models import Q # for search field
from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from .models import Product, Category


# category view
def category_detail(request, slug):
    category = get_object_or_404(Category,slug = slug)
    products = category.products.filter(status=Product.ACTIVE)
    return render(request, 'store/category_detail.html',
                  {'category':category,
                   'products':products})

# Create your views here.
def product_detail(request,category_slug,slug):
    
    product = get_object_or_404(Product, slug = slug, status=Product.ACTIVE)
    return render(request,'store/product_detail.html',{
        'product': product
    })

#    ---------add to Cart view function---------

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('cart_view')
    
#  ---------------   Change quantity      -------------------------
def change_quantity(request, product_id):
    action = request.GET.get('action','')
    
    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1 
        
        cart = Cart(request)
        cart.add(int(product_id), quantity, True)

    return redirect('cart_view')


#   ---------  Remove from cart    ---------------------------
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')
#---------------------        -------------------------



# -----------------------------------------------------

# view function for cart (we create)
def cart_view(request):
    cart = Cart(request)

    return render(request, 'store/cart_view.html', {
        'cart':cart
    })



# for Search field
def search(request):
    query = request.GET.get('query','') # get data from search fiels with name query
    products = Product.objects.filter(status=Product.ACTIVE).all()
    products = products.filter(Q(title__icontains=query)&
                                      Q(description__icontains=query))
    return render(request, 'store/search.html',{
        'query':query,
        'products':products
    })

