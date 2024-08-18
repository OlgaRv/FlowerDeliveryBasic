# C:/Users/Ольга/Documents/GitHub/FlowerDeliveryBasic/FlowerDelivery_Basic/main/views.py

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserProfileRegistrationForm, OrderForm
from .models import Flower, Order, Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from aiogram import Bot
import asyncio
from django.urls import reverse

def home(request):
    return render(request, 'main/home.html')

from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserProfileRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Создаем объект User, но пока не сохраняем его в базу данных
            user.set_password(form.cleaned_data['password'])  # Хешируем пароль
            user.save()  # Сохраняем объект User в базу данных

            # Создаем профиль, связанный с новым пользователем
            profile = Profile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', ''),  # Используем значение из формы
                address=form.cleaned_data.get('address', '')  # Используем значение из формы
            )

            login(request, user)  # Выполняем вход после регистрации
            return redirect('catalog')  # Перенаправление после успешной регистрации
    else:
        form = UserProfileRegistrationForm()

    return render(request, 'main/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Проверяем, есть ли в запросе параметр "next", чтобы перенаправить пользователя на исходную страницу
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                form.add_error(None, "Неправильное имя пользователя или пароль.")
        else:
            form.add_error(None, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = AuthenticationForm()

    # Если передан параметр "next", сохраняем его, чтобы использовать при успешной аутентификации
    next_url = request.GET.get('next', '')

    return render(request, 'main/login.html', {'form': form, 'next': next_url})


def catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'main/catalog.html', {'flowers': flowers})

@login_required
def order(request):
    flower_id = request.GET.get('flower_id')
    quantity = request.GET.get('quantity')

    # Логирование для отладки
    print(f"Received flower_id: {flower_id}, quantity: {quantity}")

    order = None

    if flower_id and quantity:
        try:
            flower = get_object_or_404(Flower, id=flower_id)
            order = Order.objects.create(
                user=request.user,
                flower=flower,
                quantity=int(quantity),
                total_price=flower.price * int(quantity),
            )
            return redirect('order_success', order_id=order.id)
        except Exception as e:
            print(f"Error occurred while creating order: {e}")

    # Если данных в запросе нет, возвращаем стандартную форму заказа
    form = OrderForm()
    flowers = Flower.objects.all()

    return render(request, 'main/order.html', {'form': form, 'flowers': flowers, 'order': order})




def send_order_to_telegram_sync(order):
    bot_token = '7398031401:AAGb1uvxXNOOa8JacOnuNSqcCKx1BdjRiJI'
    chat_id = '489126225'
    bot = Bot(token=bot_token)
    print(f"Sending order to Telegram: {order}, {bot_token}, {chat_id}")

    flower = order.flower
    message = (
        f"New order from {order.user.username}\n"
        f"Flower: {flower.name}\n"
        f"Quantity: {order.quantity}\n"
        f"Total price: {order.total_price} ₽"
    )
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"An error occurred: {e}")


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.is_active = False
    order.save()

    # Вызов синхронной функции для отладки
    send_order_to_telegram_sync(order)

    return render(request, 'main/order_success.html', {'order': order})

@login_required
def all_orders(request):
    # Получаем все заказы текущего пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'main/all_orders.html', {'orders': orders})

