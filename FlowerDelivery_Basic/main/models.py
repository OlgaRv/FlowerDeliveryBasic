from django.db import models
from django.contrib.auth.models import User

class Flower(models.Model):
    name = models.CharField('Название букета', max_length=70)
    price = models.DecimalField('Цена букета', max_digits=10, decimal_places=2)
    image = models.ImageField('Фото', upload_to='images/', blank=True)

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField('Общая стоимость заказа', max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.flower.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Данные клиента', on_delete=models.CASCADE)
    phone = models.CharField('Телефон клиента', max_length=15)
    address = models.CharField('Адрес доставки', max_length=255)
    password = models.CharField('Пароль', max_length=255, default='password')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"Profile of {self.user.username}"