from django import forms
from django.utils import timezone
from .models import Company, Address, BankDetails, JoinRequest
from django_select2.forms import ModelSelect2Widget

from django.contrib.auth import get_user_model



#==================================================================# Company #==================================================================#
#======================# Create company #======================#
class CreateCompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = ["name", "plan"]
    
#======================# Company address #======================#    
class CompanyAddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ["street", "unit", "city", "province", "postal_code", "country"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].required = False
        self.fields['country'].initial = "South Africa"
    
#======================# Company banking details #======================#    
class CompanyBankingForm(forms.ModelForm):
    
    class Meta:
        model = BankDetails
        fields = ["bank_name", "branch_name", "branch_code", "account_number"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch_name'].required = False

#======================# Join company #======================#
class JoinCompany(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=ModelSelect2Widget(
            model=Company,
            search_fields=["name__icontains"],
            attrs={
                "data-minimum-input-length": 0,
            }
        ),
        label="Select a company"
    )
    
    class Meta:
        model = JoinRequest
        fields = ["company"]


    
