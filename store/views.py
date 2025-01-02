from django.shortcuts import render
from .models import*

# Create your views here.

def store(request,category_slug=None):

    if category_slug != None:
        Product = product.objects.filter(category__slug=category_slug,is_active=True)
    else:
        Product = product.objects.filter(is_active=True)
    
    return render(request,'store/product.html',{'product':Product})