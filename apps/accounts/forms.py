from django import forms
from django.utils import timezone
from .models import Company, Address, BankDetails

from django.contrib.auth import get_user_model

User = get_user_model()

#==================================================================# Client #==================================================================#
class CreateCompanyForm(forms.ModelForm):
    # Skip checkboxes
    skip_address = forms.BooleanField(required=False, label="Skip Address Information")
    skip_banking = forms.BooleanField(required=False, label="Skip Banking Information")
    
    # Address fields
    street = forms.CharField(max_length=50, required=False, label="Street Address")
    unit = forms.CharField(max_length=50, required=False, label="Unit/Apartment (optional)")
    city = forms.CharField(max_length=50, required=False)
    province = forms.CharField(max_length=50, required=False)
    postal_code = forms.CharField(max_length=10, required=False, label="Postal Code")
    country = forms.CharField(max_length=50, required=False, initial="South Africa")
    
    # Banking details fields
    bank_name = forms.CharField(max_length=100, required=False, label="Bank Name")
    branch_name = forms.CharField(max_length=100, required=False, label="Branch Name (optional)")
    branch_code = forms.CharField(max_length=20, required=False, label="Branch Code")
    account_number = forms.CharField(max_length=20, required=False, label="Account Number")
    
    class Meta:
        model = Company
        fields = ["name", "plan"]
    
    def clean(self):
        cleaned_data = super().clean()
        skip_address = cleaned_data.get('skip_address')
        skip_banking = cleaned_data.get('skip_banking')
        
        # Validate address fields if not skipped
        if not skip_address:
            required_address_fields = ['street', 'city', 'province', 'postal_code', 'country']
            for field in required_address_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required unless you skip address information.')
        
        # Validate banking fields if not skipped
        if not skip_banking:
            required_banking_fields = ['bank_name', 'branch_code', 'account_number']
            for field in required_banking_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required unless you skip banking information.')
        
        return cleaned_data
    
    def save(self, commit=True):
        company = super().save(commit=False)
        
        if commit:
            company.save()
            
            # Create Address only if not skipped
            if not self.cleaned_data.get('skip_address'):
                Address.objects.create(
                    company=company,
                    street=self.cleaned_data['street'],
                    unit=self.cleaned_data['unit'],
                    city=self.cleaned_data['city'],
                    province=self.cleaned_data['province'],
                    postal_code=self.cleaned_data['postal_code'],
                    country=self.cleaned_data['country']
                )
            
            # Create BankDetails only if not skipped
            if not self.cleaned_data.get('skip_banking'):
                BankDetails.objects.create(
                    company=company,
                    bank_name=self.cleaned_data['bank_name'],
                    branch_name=self.cleaned_data['branch_name'],
                    branch_code=self.cleaned_data['branch_code'],
                    account_number=self.cleaned_data['account_number']
                )
        
        return company


    
