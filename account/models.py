
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class AccountManager(BaseUserManager):

    def create_user(self, firstname,lastname, username,email, password=None):
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
        
    def create_superuser(self, firstname,lastname, username,email, password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname,
            password=password,
            
            
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superadmin=True
        user.is_active=True

        user.save(using=self.db)
        return user
    
class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phonenumber=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
    
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','firstname','lastname']
    
    def has_module_perms(self,add_lable):
        return True
    
    def has_perm(self,perm,obj=None):
        return self.is_admin


    
