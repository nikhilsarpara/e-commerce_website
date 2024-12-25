from django import forms
from account.models import Account

class registerationform(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'formcontrol'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'formcontrol'}))
    class Meta:
        model = Account
        fields = ['firstname', 'lastname', 'phonenumber', 'email', 'password','confirm_password']
    
    def clean(self):
        cleaned_data=super(registerationform,self).clean()
        password= cleaned_data.get('password')
        confirm_password= cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('password and confirm password does not match')
        
    def _init_(self, *args, ** kwargs):
        super(registerationform, self) ._init_(*args, ** kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "First Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Last Namme"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Phone Number"
        self.fields['email'].widget.attrs['placeholder'] = "Email"

        for i in self.fields:
            self.fields[i].widget.attrs['class'] = "form-control"    