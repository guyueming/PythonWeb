from django import forms
from .models import WoodModel
from django.core.exceptions import ValidationError


class WoodForm(forms.Form):
    name = forms.CharField(label='名称',
                           max_length=64,
                           error_messages={'required': '名称不能为空'})
    note = forms.CharField(label='备注', max_length=256, required=False)

    def clean(self):
        value = self.cleaned_data['name']
        if WoodModel.objects.filter(name=value):
            raise ValidationError(message="名称已存在")
        else:
            return value
