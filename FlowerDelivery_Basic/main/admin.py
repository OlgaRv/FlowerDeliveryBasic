from django.contrib import admin
from .models import Flower, Profile, Order

# Register your models here.
admin.site.register(Flower)
admin.site.register(Profile)
admin.site.register(Order)