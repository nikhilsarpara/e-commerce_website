from django.shortcuts import render, redirect
from .forms import registerationform
from .models import Account
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# email libraries
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
# Create your views here.

# register view
def register(request):
    if request.method == "POST":
        form = registerationform(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['firstname']
            last_name = form.cleaned_data['lastname']
            phone_number = form.cleaned_data['phonenumber']
            email = form.cleaned_data.get('email')
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            username = email.split("@")[0]
            user = Account.objects.create_user(firstname=first_name,lastname=last_name,email=email,password=password,username=username)
            user.phone_number = phone_number
            user.save()

            try:
                email_subject = "Please Activate Your Account."
                current_site = get_current_site(request)
                context = {
                        'user':user,
                        'domain' : current_site,
                        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                        'token' : default_token_generator.make_token(user),
                    }
            
                message = render_to_string('account/verificatin_mail.html',context)
                send_email = EmailMessage(email_subject,message,to=[email])
                send_email.send()
            except:
                pass
            return redirect('/account/login/?command=verification&email='+email)
        else:
            
            messages.error(request,"User is already register")
            return register('register')
    else:
        form = registerationform()

    context = {
        'form':form,
    }
    return render(request,'account/register.html', context)

# verification view
def activate(request,uid64,token):
    try:
        userid = urlsafe_base64_decode(uid64).decode()
        user = Account._default_manager.get(id=userid)
        tokens = default_token_generator.check_token(user,token)
    except:
        user = None
    
    if user is not None and tokens:
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

# login view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'login success')
            return redirect('index')
    return render(request,'account/login.html')




# def register(request):
#     if request.method == 'POST':
#         forms = registerationform(request.POST)
#         if forms.is_valid():
#             firstname = forms.cleaned_data['firstname']
#             lastname = forms.cleaned_data['lastname']
#             email = forms.cleaned_data['email']
#             phonenumber = forms.cleaned_data['phonenumber']
#             password = forms.cleaned_data['password']
#             confirm_password = forms.cleaned_data['confirm_password']

#             if password != confirm_password:
#                 forms.add_error('confirm_password', "Passwords do not match.")
#             else:
#                 username = email.split('@')[0]
#                 user = Account.objects.create_user(
#                     firstname=firstname,
#                     lastname=lastname,
#                     email=email,
#                     password=password,
#                     username=username
#                 )
#                 user.phonenumber = phonenumber
#                 user.save()
#                 # send email
#                 email_suject='please activate your account'
#                 current_site=get_current_site(request)
#                 message= render_to_string('account/verificatin_mail.html',{
#                     'user':user,
#                     'domain':current_site,
#                     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token':default_token_generator.make_token(user),
#                 })

#                 send_email=EmailMessage(email_suject,message,to=[email])
#                 send_email.send()
#                 messages.success(request,'login success')
#                 return redirect('login')
#     else:
#         forms = registerationform()
    
#     context = {
#         'form': forms
#     }
#     return render(request, 'account/register.html',context)