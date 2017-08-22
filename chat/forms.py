from django import forms
from .models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    code = forms.CharField(max_length=100)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username', 'email', 'code']