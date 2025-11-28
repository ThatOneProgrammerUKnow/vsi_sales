from django import forms
from django.utils import timezone
from .models import Client, Product, Order, OrderItem, Invoice
from django.forms.models import inlineformset_factory

#=====# Client #=====#
class ClientForm(forms.ModelForm):
    class Meta: 
        model = Client
        exclude = ["id", "company"]

#=====# Product #=====#
class ProductForm(forms.ModelForm):
    class Meta: 
        model = Product
        exclude = ["id", "company", "updated_at"]

#=====# Order #=====#
class OrderForm(forms.ModelForm):
    class Meta: 
        model = Order
        exclude = ["company"]

        widgets = {
        'date': forms.DateInput(attrs={
        'class': 'form-control',
            'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()


#=====# Invoice #=====#
class InvoiceForm(forms.ModelForm):
    class Meta: 
        exclude = [""]
        model = Invoice
        widgets = {
        'pay_by_date': forms.DateInput(attrs={
        'class': 'form-control',
            'type': 'date'
            }),
        }