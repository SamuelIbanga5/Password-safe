from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import PasswordSafe
User = get_user_model()

class UserCreateForm(UserCreationForm):
     
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(UserChangeForm):
        
    class Meta:
        model = User
        fields = ['avatar', 'username', 'first_name', 'last_name', 'email']
        exclude = ('password',)

class PasswordSafeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=50)

    class Meta:
        model = PasswordSafe
        fields = ['site_name', 'site', 'email']
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }