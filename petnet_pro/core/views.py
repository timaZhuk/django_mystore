from django.shortcuts import render

# Create your views here.
# Then we have to add this view to main url.py inside petnet_pro

#1 view for frontpage
def frontpage(request):
    return render(request, 'core/frontpage.html')

#2 view for about
def about(request):
    return render(request,'core/about.html') 