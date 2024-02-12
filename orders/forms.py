from urllib import request

from django import forms
from orders.models import Order
from users.models import User


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ilia'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'kavaleu'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'code.ninja.code1@gmail.com'}))
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Poland, Gdansk, ul.Niepodleglosci, d689'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')