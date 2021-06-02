from django.contrib import admin

# Register your models here.
from .models import PaperModel, PaperFormModel

admin.site.register(PaperModel)
admin.site.register(PaperFormModel)
