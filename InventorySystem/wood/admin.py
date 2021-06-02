from django.contrib import admin

# Register your models here.
from .models import WoodModel, WoodFormModel

admin.site.register(WoodModel)
admin.site.register(WoodFormModel)
