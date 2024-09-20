import re
from django import forms
from django.contrib.auth.hashers import make_password

from .models import CustomUser



class BaseUserForm(forms.ModelForm):
    """ Base form for common user validations """

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        
        return email


class PasswordVaildationMixin:
    """" Mixin for password validation logic """

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
    

class UserCreateForm(BaseUserForm, PasswordVaildationMixin):
    """ Form for creating user profile """

    class Meta(BaseUserForm.Meta):
        fields = BaseUserForm.Meta.fields + ['password']    

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user
    

class UserUpdateForm(BaseUserForm):
    """ Form for updating user profile (excluding password) """    

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)

        if commit:
            user.save()

        return user
    

class PasswordChangeForm(forms.Form, PasswordVaildationMixin):
    """ Form for updating user password """

    old_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")
        
        return old_password
    
    def clean_new_password(self):
        return self.clean_password()
    

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password'])

        if commit:
            self.user.save()

        return self.user