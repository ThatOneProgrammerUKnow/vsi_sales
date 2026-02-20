from django import forms
from .models import Company, Address, BankDetails, JoinRequest, User
from django_select2.forms import ModelSelect2Widget



#==================================================================# User #==================================================================#
#======================# Personal information #======================#
class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "identification_number"]

        help_texts = {
            "username" : ""
        }

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
class JoinCompanyForm(forms.ModelForm):
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


    
