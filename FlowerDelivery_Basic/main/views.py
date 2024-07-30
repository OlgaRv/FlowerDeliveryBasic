from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, OrderForm
from .models import Flower, Order
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('catalog')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'catalog.html', {'flowers': flowers})

@login_required
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            form.save_m2m()
            # Add Telegram bot integration here
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'order.html', {'form': form})

def order_success(request):
    return render(request, 'order_success.html')
