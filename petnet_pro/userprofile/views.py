from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Userprofile
from django.shortcuts import render, redirect
# Create your views here.
#-------------------------------------------------------------
def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    return render(request,'userprofile/vendor_detail.html',
    {
        'user':user
     
     })
#---------for User-pages---------------------------------------------------
@login_required
def my_store(request):
    return render(request,'userprofile/my_store.html')
#-----------------------------------------------------------
@login_required
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
            userprofile = Userprofile.objects.create(user=user)
            return redirect('frontpage')
    else:
        # if data wrong or error Form is empty in this case
        form = UserCreationForm()
    
    return render(request,'userprofile/signup.html',{
        'form':form
    })


