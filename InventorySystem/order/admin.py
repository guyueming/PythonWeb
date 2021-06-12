from django.contrib import admin

# Register your models here.

from .models import OrderModel, WoodFormModel, SkinFormModel, PaperFormModel

admin.site.register(OrderModel)
admin.site.register(WoodFormModel)
admin.site.register(SkinFormModel)
admin.site.register(PaperFormModel)