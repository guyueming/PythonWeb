from django import forms
from .models import SalesmanModel
from django.core.exceptions import ValidationError


class SalesmanForm(forms.Form):
    name = forms.CharField(label='名称',
                           max_length=64,
                           error_messages={'required': '名称不能为空'})
    phone = forms.CharField(label='电话', max_length=64, required=False)
    note = forms.CharField(label='备注', max_length=256, required=False)

    def clean_name(self):
        value = self.cleaned_data['name']
        if SalesmanModel.objects.filter(name=value):
            raise ValidationError(message="名称已存在")
        else:
            return value
