import re
from django import forms
from django.contrib.auth.hashers import make_password

from .models import CustomUser


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        
        return email
    

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError("Password must be at list 8 characters long.")
        
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at list one lowercase letter.")
        
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at list one uppercase letter.")
        
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at list one number.")
        
        if not re.search(r'[\W_]', password):
            raise forms.ValidationError("Password must contain at list one special character.")

        return password
    

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user