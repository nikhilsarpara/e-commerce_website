from django.shortcuts import render,redirect
from store.models import product

def index(request):

    pro = product.objects.all().order_by('created_at')

    context = {
        'product':pro,
    }
    return render(request,'index.html',context)

def base(request):
    return render(request,'base.html')