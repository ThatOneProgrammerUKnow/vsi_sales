from django import forms
from django.utils import timezone
from .models import GRN, Customer


class GRNForm(forms.ModelForm):
    class Meta:
        model = GRN
        fields = ['grn_number', 'date_returned', 'customer']
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

