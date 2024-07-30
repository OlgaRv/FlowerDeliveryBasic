from django import forms
from django.contrib.auth.models import User
from .models import Order, Flower

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class OrderForm(forms.ModelForm):
    flowers = forms.ModelMultipleChoiceField(queryset=Flower.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Order
        fields = ['flowers']
