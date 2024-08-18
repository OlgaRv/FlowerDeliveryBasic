from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, OrderForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'main/order.html', {'form': form})
