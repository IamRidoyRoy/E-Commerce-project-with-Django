from ast import Or
from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register model here
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)
