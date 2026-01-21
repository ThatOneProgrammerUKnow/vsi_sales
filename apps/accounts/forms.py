from django import forms
from django.utils import timezone
from .models import Company, Address, BankDetails

from django.contrib.auth import get_user_model



#==================================================================# Client #==================================================================#
class CreateCompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = ["name", "plan"]
    
class CompanyAddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ["street", "unit", "city", "province", "postal_code", "country"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].required = False
        self.fields['country'].initial = "South Africa"
    
class CompanyBankingForm(forms.ModelForm):
    
    class Meta:
        model = BankDetails
        fields = ["bank_name", "branch_name", "branch_code", "account_number"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch_name'].required = False


    
