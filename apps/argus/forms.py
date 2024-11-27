from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from account.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.check_and_set_admin_status()
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)