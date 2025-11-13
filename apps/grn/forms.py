from django import forms
from django.utils import timezone
from .models import GRN, Customer, GoodsItem
from django.forms import inlineformset_factory


class GRNForm(forms.ModelForm):
    class Meta:
        model = GRN
        fields = ['grn_number', 'date_returned', 'contact_person']
        widgets = {
            'date_returned': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date_returned'].initial = timezone.now().date()

class GoodsItemForm(forms.ModelForm):
    class Meta:
        model = GoodsItem
        fields = ['type_of_good', 'serial_number', 'model_number', 'description']

GoodsFormset = inlineformset_factory(GRN, GoodsItem, form=GoodsItemForm, extra=1)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'branch']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer Name'
            }),
            'branch': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Branch (optional)'
            }),
        }
