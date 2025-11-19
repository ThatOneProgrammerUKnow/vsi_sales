from django import forms
from django.utils import timezone
from .models import GRN, Customer, GoodsItem, ContactPerson
from django.forms import inlineformset_factory

#--->>> GRN Form 
# GRN Part
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
            
# Goods formset
class GoodsItemForm(forms.ModelForm):
    class Meta:
        model = GoodsItem
        fields = ['type_of_good', 'serial_number', 'model_number', 'description']

GoodsFormset = inlineformset_factory(GRN, GoodsItem, form=GoodsItemForm, extra=1)

#--->>> Customer form
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
# Contact Person formset
class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ['name', 'surname', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Name'
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Surname'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Email'
            }),
        }

class AddContactPersonForm(ContactPersonForm):
    class Meta(ContactPersonForm.Meta):
        fields = ContactPersonForm.Meta.fields + ['customer']




