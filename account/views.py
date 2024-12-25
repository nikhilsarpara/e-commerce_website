from django.shortcuts import render, redirect
from .forms import registerationform
from .models import Account
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
# email libraries
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
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
                # send email
                email_suject='please activate your account'
                current_site=get_current_site(request)
                message= render_to_string('account/verificatin_mail.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                })

                send_email=EmailMessage(email_suject,message,to=[email])
                send_email.send()

                return redirect('login')
    else:
        forms = registerationform()
    
    context = {
        'form': forms
    }
    return render(request, 'account/register.html',context)

def activate(request,uid,token):
    pass    

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            user.save()
            return redirect('index')
    return render(request,'account/login.html')
