from django import forms
from .models import TechnologyModel, SpecificationModel
from django.core.exceptions import ValidationError


class TechnologyForm(forms.Form):
    name = forms.CharField(label='名称',
                           max_length=64,
                           error_messages={'required': '名称不能为空'})
    note = forms.CharField(label='备注', max_length=256, required=False)

    def clean_name(self):
        value = self.cleaned_data['name']
        if TechnologyModel.objects.filter(name=value):
            raise ValidationError(message="名称已存在")
        else:
            return value


class SpecificationForm(forms.Form):
    name = forms.CharField(label='名称',
                           max_length=64,
                           error_messages={'required': '名称不能为空'})
    note = forms.CharField(label='备注', max_length=256, required=False)

    def clean_name(self):
        value = self.cleaned_data['name']
        if SpecificationModel.objects.filter(name=value):
            raise ValidationError(message="名称已存在")
        else:
            return value
