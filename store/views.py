from django.shortcuts import render
from .models import*
from django.http import HttpResponse

# Create your views here.

def store(request,category_slug=None):

    if category_slug != None:
        Product = product.objects.filter(category__slug=category_slug,is_active=True)
        count=Product.count()
    else:
        Product = product.objects.filter(is_active=True)
        count=Product.count()

    context={
        'product':Product,
        'product_count':count,
        }
    return render(request,'store/product.html',context)

def product_details(request,category_slug,product_slug):
    p_product = product.objects.get(category__slug=category_slug,slug=product_slug)
    context={
        'product_detail':p_product,
    }
    return render(request,'store/product_detail.html',context)
