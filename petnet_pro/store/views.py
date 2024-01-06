import json
import stripe

from django.conf import settings
from django.db.models import Q # for search field
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .cart import Cart
from .forms import OrderForm
from .models import Product, Category, Order, OrderItems



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

# view function for success rsponse payment
def success(request):
    return render(request,'store/success.html')

#---Check out whether user authenticated or not
@login_required
def checkout(request):
    cart = Cart(request)
    form = OrderForm()
    if cart.get_total_cost() == 0:
        return redirect('cart_view')
    #---------------------------
    if request.method == 'POST':
        a=True
        data = json.loads(request.body)
        first_name = data['first_name']
        last_name = data['last_name']
        address = data['address']
        zipcode = data['zipcode']
        city = data['city']
        form = OrderForm(request.POST)
        total_price = 0
        items = [] # for payment method
        if a==True and first_name and last_name and address and zipcode and city:
            
            
            #--loop through the cart (future order)
            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])
                #add all items in the cart
                items.append({
                    'price_data':{
                        'currency':'usd',
                        'product_data':{
                            'name':product.title
                        },
                        'unit_amount':product.price
                    },
                    'quantity':item['quantity']
                })
            #stripe Secret Key
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session=stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=items,
                mode='payment',
                success_url = settings.WEBSITE_URL+'cart/success/',
                cancel_url = settings.WEBSITE_URL+'cart/'
            ) 
            #---create stripe payment session
            # ---payment intent from stripe
            payment_intent = session.payment_intent
            # -create order object
            # -commit = False we don't want to save anything in dataBase
            #order = form.save(commit = False) # Order.objects.create()
            order = Order.objects.create(
            first_name = first_name, #data['first_name'],
            last_name = last_name, #data['last_name'],
            address = address, #data['address'],
            zipcode = zipcode, #data['zipcode'],
            city = city, #data['city'],
            paid_amount = total_price,
            is_paid = True,
            payment_intent = payment_intent, 
            created_by = request.user
            )
            
            #order.save()
            # -create new order in DB
            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity
                item = OrderItems.objects.create(order = order,
                                                 product = product,price = price,
                                                 quantity = quantity)
            cart.clear()



            return JsonResponse({'session':session,
                                 'order':payment_intent
                                 })#redirect('myaccount')
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html',{
        'cart':cart,
        'form':form,
        'pub_key':settings.STRIPE_PUB_KEY
    })


# for Search field
def search(request):
    query = request.GET.get('query','') # get data from search fields with name query
    products = Product.objects.filter(status=Product.ACTIVE).all()
    products = products.filter(Q(title__icontains=query)&
                                      Q(description__icontains=query))
    return render(request, 'store/search.html',{
        'query':query,
        'products':products
    })

