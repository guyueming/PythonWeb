import time

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm, BaseInlineFormSet
from django.forms import inlineformset_factory
from django.utils import formats

from wood.models import WoodModel
from paper.models import PaperModel
from .models import OrderModel, OrderHeadModel, OrderNumberModel, FORM_TYPE


class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list

    def render(self, name, value, attrs=None, renderer=None):
        default_attrs = {'list': 'list__%s' % self._name}
        if attrs:
            default_attrs.update(attrs)
        text_html = super(ListTextWidget, self).render(name, value, attrs=default_attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item.id
            data_list += '%s</option>' % item
        data_list += '</datalist>'

        return text_html + data_list


def query_paper(name):
    str_s = name.split('~')
    if len(str_s) == 3:
        q = (Q(color=str_s[0]))
        q.add(Q(type=str_s[1]), Q.AND)
        q.add(Q(factory=str_s[2]), Q.AND)
        return PaperModel.objects.filter(q).first()
    return None


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderHeadForm(ModelForm):
    class Meta:
        model = OrderHeadModel
        fields = ("order_number", "order_date", "delivery_date", "salesman", "customer")
        widgets = {
            'order_number': forms.TextInput(attrs={"style": "width:120; height:24px;", "readonly": "readonly"}),
            'order_date': forms.DateInput(format='%Y-%m-%d',
                                          attrs={'type': 'date', 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl'}),
            'delivery_date': forms.DateInput(format='%Y-%m-%d',
                                             attrs={'type': 'date', 'pattern=': '\d{4}-\d{2}-\d{2}', }),
        }


class OrderModelForm(ModelForm):
    class Meta:
        model = OrderModel
        fields = '__all__'

    # def clean_paper(self):
    #     value = self.cleaned_data['paper']
    #     print(value)
    #     value = query_paper(value)
    #     if not value:
    #         raise ValidationError(message="纸张选择错误")
    #     else:
    #         return value.id


class OrderBaseInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(OrderBaseInlineFormSet, self).add_fields(form, index)
        form.fields['woodCount'].widget = forms.NumberInput(attrs={"style": "width:60; height:24px;"})
        form.fields['skinCount'].widget = forms.NumberInput(attrs={"style": "width:60; height:24px;"})
        form.fields['other_skin_count'].widget = forms.NumberInput(attrs={"style": "width:60; height:24px;"})
        form.fields['paper'].widget = ListTextWidget(attrs={"style": "width:120; height:24px;"},
                                                     name='paper',
                                                     data_list=PaperModel.objects.filter(enable=True))
        form.fields['other_paper'].widget = ListTextWidget(attrs={"style": "width:120; height:24px;"},
                                                           name='other_paper',
                                                           data_list=PaperModel.objects.filter(enable=True))
        form.fields['paperCount'].widget = forms.NumberInput(attrs={"style": "width:60; height:24px;"})
        form.fields['other_paper_count'].widget = forms.NumberInput(attrs={"style": "width:60; height:24px;"})
        form.fields['packaging'].widget = forms.TextInput(attrs={"style": "width:60; height:24px;/"})
        form.fields['thickness'].widget = forms.TextInput(attrs={"style": "width:60; height:24px;"})
        form.fields['trademark'].widget = forms.TextInput(attrs={"style": "width:60; height:24px;"})
        form.fields['word'].widget = forms.TextInput(attrs={"style": "width:60; height:24px;"})
        form.fields['note'].widget = forms.Textarea(attrs={"style": "width:80; height:24px;"})
        form.fields['wood'].widget.attrs = {"style": "width:80; height:24px;"}

    # def clean(self):
    #     # get forms that actually have valid data
    #     count = 0
    #     delete_checked = 0
    #     for form in self.forms:
    #         try:
    #             if form.cleaned_data:
    #                 count += 1
    #                 if form.cleaned_data['DELETE']:
    #                     delete_checked += 1
    #                 if not form.cleaned_data['DELETE']:
    #                     delete_checked -= 1
    #         except AttributeError:
    #             # annoyingly, if a subform is invalid Django explicity raises
    #             # an AttributeError for cleaned_data
    #             pass
    #
    #     # Case no images uploaded
    #     if count < 1:
    #         raise forms.ValidationError(
    #             'At least one image is required.')
    #
    #     # Case one image added and another deleted
    #     if delete_checked > 0 and OrderModel.objects.filter(product=self.instance).count() == 1:
    #         raise forms.ValidationError("At least one image is required.")


OrderFormSet = inlineformset_factory(OrderHeadModel, OrderModel, OrderModelForm, OrderBaseInlineFormSet,
                                     exclude=['user', 'created_time'],
                                     extra=1, can_delete=True)

ViewOrderFormSet = inlineformset_factory(OrderHeadModel, OrderModel, OrderModelForm, OrderBaseInlineFormSet,
                                         exclude=['user', 'created_time'],
                                         extra=0, can_delete=True)

