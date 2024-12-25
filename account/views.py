from django.shortcuts import render, redirect
from .forms import registerationform
from .models import Account
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def register(request):
    if request.method == 'POST':
        forms = registerationform(request.POST)
        if forms.is_valid():
            firstname = forms.cleaned_data['firstname']
            lastname = forms.cleaned_data['lastname']
            email = forms.cleaned_data['email']
            phonenumber = forms.cleaned_data['phonenumber']
            password = forms.cleaned_data['password']
            confirm_password = forms.cleaned_data['confirm_password']

            if password != confirm_password:
                forms.add_error('confirm_password', "Passwords do not match.")
            else:
                username = email.split('@')[0]
                user = Account.objects.create_user(
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    password=password,
                    username=username
                )
                user.phonenumber = phonenumber
                user.save()
                return redirect('login')
    else:
        forms = registerationform()
    
    context = {
        'form': forms
    }
    return render(request, 'account/register.html',context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request,email=email,password=password)
        if user is not None:
            auth.login(request,user)
            user.save()
        return redirect('index')
    return render(request,'account/login.html')
