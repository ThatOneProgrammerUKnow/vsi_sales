from django import forms
from django.utils import timezone
from .models import Client, Product, Order, OrderItem, Invoice, Status
from django.forms.models import inlineformset_factory
from django.contrib.auth import get_user_model

User = get_user_model()

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
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()

        self.fields["status"].queryset = Status.objects.filter(company=user.company)
        self.fields["client"].queryset = Client.objects.filter(company=user.company)

#=====# OrderItem Form #=====#
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "qty", "discount"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # get user from view
        super().__init__(*args, **kwargs)
        # Filter product dropdown to only products in this user's company
        self.fields['product'].queryset = Product.objects.filter(company=user.company)

#=====# OrderItem Formset #=====#
OrderItemFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderItem,
    form = OrderItemForm,
    fields=["product", "qty", "discount"],
    extra=1,
    can_delete=True,
)

#=====# Invoice #=====#
class InvoiceForm(forms.ModelForm):
    class Meta: 
        fields = ["date", "pay_by_date"]
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