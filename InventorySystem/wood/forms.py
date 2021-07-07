from django import forms
from django.forms import ModelForm

from .models import WoodModel
from order.models import WoodFormModel
from django.core.exceptions import ValidationError


class WoodForm(forms.Form):
    name = forms.CharField(label='名称',
                           max_length=64,
                           error_messages={'required': '名称不能为空'})
    factory = forms.CharField(label='厂家', max_length=64, required=False)
    note = forms.CharField(label='备注', max_length=256, required=False)

    def clean_name(self):
        value = self.cleaned_data['name']
        if WoodModel.objects.filter(name=value):
            raise ValidationError(message="名称已存在")
        else:
            return value

    def save(self):
        dic = {"name": self.cleaned_data['name'], "note": self.cleaned_data['note'],
               "factory": self.cleaned_data['factory']}
        return WoodModel.objects.create(**dic)


class WoodOrderForm(ModelForm):
    class Meta:
        model = WoodFormModel
        fields = ['name', 'arrive_date', 'count', 'type']
