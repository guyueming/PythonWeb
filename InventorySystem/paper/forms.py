from django import forms
from django.db.models import Q

from .models import PaperModel
from django.core.exceptions import ValidationError


class PaperForm(forms.Form):
    name = forms.CharField(label='名称',
                           max_length=64,
                           error_messages={'required': '名称不能为空'})
    color = forms.CharField(label='花色', max_length=64)
    type = forms.CharField(label='型号', max_length=64)
    factory = forms.CharField(label='厂家', max_length=64)
    note = forms.CharField(label='备注', max_length=256, required=False)

    def clean(self):
        cleaned_data = super(PaperForm, self).clean()
        name = self.cleaned_data.get('name')
        q = Q(name=name)
        color = self.cleaned_data.get('color')
        q.add(Q(color=color), Q.AND)
        tp = self.cleaned_data.get('type')
        q.add(Q(type=tp), Q.AND)
        factory = self.cleaned_data.get('factory')
        if factory:
            q.add(Q(factory=factory), Q.AND)
        print(q)
        if PaperModel.objects.filter(q):
            self.add_error("name", "存在相同纸张")
        else:
            return cleaned_data
