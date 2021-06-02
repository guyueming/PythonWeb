from django.contrib import admin

# Register your models here.
from .models import TechnologyModel, SpecificationModel

admin.site.register(TechnologyModel)
admin.site.register(SpecificationModel)
