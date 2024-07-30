from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, OrderForm
from .models import Flower, Order
from django.contrib.auth.decorators import login_required
from aiogram import Bot
import asyncio

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
    return render(request, 'main/register.html', {'form': form})

def catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'main/catalog.html', {'flowers': flowers})

@login_required
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            form.save_m2m()
            send_order_to_telegram(order)
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'main/order.html', {'form': form})

def order_success(request):
    return render(request, 'main/order_success.html')

def send_order_to_telegram(order):
    bot_token = 'AAGb1uvxXNOOa8JacOnuNSqcCKx1BdjRiJI'
    chat_id = 'BunchMag_bot'
    bot = Bot(token=bot_token)
    message = f"New order from {order.user.username}\nFlowers: {[flower.name for flower in order.flowers.all()]}"
    asyncio.run(bot.send_message(chat_id=chat_id, text=message))
