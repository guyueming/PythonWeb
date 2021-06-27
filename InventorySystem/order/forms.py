from django import forms
from django.forms import ModelForm, BaseInlineFormSet
from django.forms import inlineformset_factory
from wood.models import WoodModel
from .models import OrderModel, OrderHeadModel, OrderNumberModel, FORM_TYPE


class OrderHeadForm(ModelForm):
    class Meta:
        model = OrderHeadModel
        fields = ("order_number", "order_date", "delivery_date", "salesman", "customer")


class OrderModelForm(ModelForm):
    class Meta:
        model = OrderModel
        fields = '__all__'
        # fields = ['wood', 'woodCount', 'skin', 'skinCount', 'paper', 'paperCount', 'other_paper', 'other_paper_count',
        #           'packaging', 'thickness', 'trademark', 'word', 'note']


class OrderBaseInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(OrderBaseInlineFormSet, self).add_fields(form, index)
        form.fields['woodCount'].widget = forms.NumberInput(attrs={"style": "width:60"})
        form.fields['skinCount'].widget = forms.NumberInput(attrs={"style": "width:60"})
        form.fields['paperCount'].widget = forms.NumberInput(attrs={"style": "width:60"})
        form.fields['other_paper_count'].widget = forms.NumberInput(attrs={"style": "width:60"})
        form.fields['packaging'].widget = forms.TextInput(attrs={"style": "width:60"})
        form.fields['thickness'].widget = forms.TextInput(attrs={"style": "width:60"})
        form.fields['trademark'].widget = forms.TextInput(attrs={"style": "width:60"})
        form.fields['word'].widget = forms.TextInput(attrs={"style": "width:60"})
        form.fields['note'].widget = forms.TextInput(attrs={"style": "width:80"})
        form.fields['wood'].widget.attrs = {"style": "width:80"}
        form.fields['paper'].widget.attrs = {"style": "width:120"}
        form.fields['other_paper'].widget.attrs = {"style": "width:120"}


OrderFormSet = inlineformset_factory(OrderHeadModel, OrderModel, OrderModelForm, OrderBaseInlineFormSet,
                                     exclude=['user', 'created_time'],
                                     extra=1, can_delete=True)


class OrdersForm(forms.Form):
    order_date = forms.DateField(label="下单日期")
    delivery_date = forms.DateField(label="交货日期")
    salesman = forms.DateField(label="销售")
    customer = forms.DateField(label="客户")
    note = forms.DateField(label="备注")
