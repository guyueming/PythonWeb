import time

from django import forms
from django.forms import ModelForm, BaseInlineFormSet
from django.forms import inlineformset_factory
from wood.models import WoodModel
from .models import OrderModel, OrderHeadModel, OrderNumberModel, FORM_TYPE


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


class OrderBaseInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(OrderBaseInlineFormSet, self).add_fields(form, index)
        form.fields['woodCount'].widget = forms.NumberInput(attrs={"style": "width:60; height:24px;"})
        form.fields['skinCount'].widget = forms.NumberInput(attrs={"style": "width:60; height:24px;"})
        form.fields['paperCount'].widget = forms.NumberInput(attrs={"style": "width:60; height:24px;"})
        form.fields['other_paper_count'].widget = forms.NumberInput(attrs={"style": "width:60; height:24px;"})
        form.fields['packaging'].widget = forms.TextInput(attrs={"style": "width:60; height:24px;/"})
        form.fields['thickness'].widget = forms.TextInput(attrs={"style": "width:60; height:24px;"})
        form.fields['trademark'].widget = forms.TextInput(attrs={"style": "width:60; height:24px;"})
        form.fields['word'].widget = forms.TextInput(attrs={"style": "width:60; height:24px;"})
        form.fields['note'].widget = forms.Textarea(attrs={"style": "width:80; height:24px;"})
        form.fields['wood'].widget.attrs = {"style": "width:80; height:24px;"}
        form.fields['paper'].widget.attrs = {"style": "width:120; height:24px;"}
        form.fields['other_paper'].widget.attrs = {"style": "width:120; height:24px;"}

    def clean(self):
        # get forms that actually have valid data
        count = 0
        delete_checked = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
                    if form.cleaned_data['DELETE']:
                        delete_checked += 1
                    if not form.cleaned_data['DELETE']:
                        delete_checked -= 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass

        # Case no images uploaded
        if count < 1:
            raise forms.ValidationError(
                'At least one image is required.')

        # Case one image added and another deleted
        if delete_checked > 0 and OrderModel.objects.filter(product=self.instance).count() == 1:
            raise forms.ValidationError("At least one image is required.")


OrderFormSet = inlineformset_factory(OrderHeadModel, OrderModel, OrderModelForm, OrderBaseInlineFormSet,
                                     exclude=['user', 'created_time'],
                                     extra=1, can_delete=True)

ViewOrderFormSet = inlineformset_factory(OrderHeadModel, OrderModel, OrderModelForm, OrderBaseInlineFormSet,
                                         exclude=['user', 'created_time'],
                                         extra=0, can_delete=True)

