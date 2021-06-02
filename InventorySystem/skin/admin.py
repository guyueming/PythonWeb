from django.contrib import admin

# Register your models here.
from .models import SkinModel, SkinFormModel

admin.site.register(SkinModel)
admin.site.register(SkinFormModel)
