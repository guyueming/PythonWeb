from django.contrib import admin

# Register your models here.
from .models import CustomerModel

admin.site.register(CustomerModel)
