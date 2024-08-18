# C:/Users/Ольга/Documents/GitHub/FlowerDeliveryBasic/FlowerDelivery_Basic/main/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Profile, Flower, Order


class UserProfileRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Имя пользователя')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=15, label='Телефон')
    address = forms.CharField(max_length=255, label='Адрес')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'phone', 'address']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают.')

        return cleaned_data

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
        return user

class OrderForm(forms.ModelForm):
    flower = forms.ModelChoiceField(queryset=Flower.objects.all(), to_field_name="id")
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = Order
        fields = ['flower', 'quantity']
        labels = {
            'flower': 'Выберите букет',
            'quantity': 'Количество'
        }

    def save(self, commit=True, user=None):
        order = super().save(commit=False)
        order.user = user
        order.total_price = self.cleaned_data['flower'].price * self.cleaned_data['quantity']
        if commit:
            order.save()
        return order
