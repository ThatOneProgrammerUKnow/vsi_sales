from django import forms
from django.utils import timezone
from .models import Client, Product, Order, OrderItem, Invoice, Status
from django.forms.models import inlineformset_factory

#=====# Client #=====#
class ClientForm(forms.ModelForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '+27844557832'}))
    class Meta: 
        model = Client
        fields = ["name", "surname", "phone_number", "email", "vat_number", "vat_verified"]

#=====# Product #=====#
class ProductForm(forms.ModelForm):
    class Meta: 
        model = Product
        # Exclude computed field from the form
        exclude = ["id", "company", "updated_at", "price_after_vat"]


#=====# Order #=====#
class OrderForm(forms.ModelForm):
    class Meta: 
        model = Order
        exclude = ["company", "updated_at"]

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

#=====# OrderItem Formset #=====#
# Inline formset linking Order -> OrderItem, using the OrderItemForm above.
OrderItemFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderItem,
    fields=["product", "qty"],
    extra=1,
    can_delete=True,
)




#=====# Invoice #=====#
class InvoiceForm(forms.ModelForm):
    class Meta: 
        exclude = ["updated_at"]
        model = Invoice
        widgets = {
        'pay_by_date': forms.DateInput(attrs={
        'class': 'form-control',
            'type': 'date'
            }),
        'date': forms.DateInput(attrs={
        'class': 'form-control',
            'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["date"].initial = timezone.now().date()

#=====# Status #=====#
class StatusForm(forms.ModelForm):
    class Meta: 
        model = Status
        fields = ["status"]