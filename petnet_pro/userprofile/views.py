#for messages for user
from django.contrib import messages
#for login
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Userprofile
from django.shortcuts import render, redirect
from django.utils.text import slugify
# Create your views here.
from store.forms import ProductForm 
from store.models import Product
#-------------------------------------------------------------
def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)
    return render(request,'userprofile/vendor_detail.html',
    {
        'user':user,
        'products':products
     
     })
#---------for User-pages----Main Page of Account-----------------------------------------------
@login_required # want user was authenticated
def my_store(request):
    # we exclude from my_store all items with status='DELETEED'
    products = request.user.products.exclude(status=Product.DELETED)
    return render(request,'userprofile/my_store.html',
    {
    'products':products
                  })
#----------------Editing-Adding--Deleting----------------------------------------
@login_required
def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            title = request.POST.get('title') # we get title from our request
            slug = slugify(title)
            # we create a instance of product
            product = form.save(commit=False) # but it doesn't add to DB
            product.user = request.user # we save requsted user in DB
            product.slug = slug # add product's slug to DB
            #Then we can add product to DB
            product.save()
            # success message
            messages.success(request, 'New product was added')
            # redirect to my-store to User's account
            return redirect('my_store') # name='my_store' in urls
        else:
            form = ProductForm()
    return render(request, 'userprofile/product_form.html', {
        'title':'Add product',
        'form':form
    })

# For editing particular product (thet was added before)
@login_required
def edit_product(request, pk):
    # filter(user=request.user we choose only user who is authenticated
    # in system
    product = Product.objects.filter(user=request.user).get(pk=pk)
    #form = ProductForm(instance = product) #instance = product
    if request.method=="POST":
        # we overwrite old values in product
        form = ProductForm(request.POST, request.FILES, instance = product)
        if form.is_valid():
            form.save()
            # message that product was edited
            messages.success(request, 'Product was editted')
            # we don't need to add all fields for product
            # redirect to my-store to User's account
            return redirect('my_store')

    else:
        form = ProductForm(instance = product)

    return render(request,'userprofile/product_form.html',{
        'title':'Edit product',
        'product':product,
        'form':form
    })

# instead of deleting we add status 'Delete' in stoore.models
# then we change the status by 'delete_product'
@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user = request.user).get(pk=pk)
    # Change the status of this product
    product.status = Product.DELETED
    product.save()
    messages.success(request, 'Product was deleted!')
    return redirect('my_store')


#------------My Account View----------------------------------------@login_required
def myaccout(request):
    return render(request, 'userprofile/myaccount.html')
#------------------------------------------------------------

# craete view for sign up
def signup(request):
    # if we have POST method (in form)
    if request.method == 'POST':
        #create object form
        form = UserCreationForm(request.POST)
        # if all fields in form valid
        if form.is_valid():
            # we create user data and save
            user = form.save()
            #save user (login)
            login(request, user)
            #create userprofile
            userprofile = Userprofile.objects.create(user = user)
            return redirect('frontpage')
    else:
        # if data wrong or error Form is empty in this case
        form = UserCreationForm()
    
    return render(request,'userprofile/signup.html',{
        'form':form
    })


