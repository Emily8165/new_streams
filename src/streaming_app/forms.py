from django import forms

from . import models


class LoginForm(forms.Form):
    name = forms.CharField(label="User Name", max_length=255, required=False)
    email = forms.EmailField(label="Email", max_length=255, required=False)
    password = forms.CharField(
        label="Password", max_length=255, widget=forms.PasswordInput()
    )

    class Meta:
        model = models.Listener
        fields = ["name", "email", "password"]
