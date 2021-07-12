from django import forms
from .models import SkinModel
from django.core.exceptions import ValidationError


class SkinForm(forms.Form):
    name = forms.CharField(label='名称',
                           max_length=64,
                           error_messages={'required': '名称不能为空'})
    factory = forms.CharField(label='厂家', max_length=64, required=False)
    note = forms.CharField(label='备注', max_length=256, required=False)
    count = forms.IntegerField(label='数量', initial=0, required=False)

    def clean_name(self):
        value = self.cleaned_data['name']
        if SkinModel.objects.filter(name=value):
            raise ValidationError(message="名称已存在")
        else:
            return value

    def save(self):
        dic = {"name": self.cleaned_data['name'], "note": self.cleaned_data['note'],
               "factory": self.cleaned_data['factory'], "count": self.cleaned_data['count']}
        SkinModel.objects.create(**dic)
