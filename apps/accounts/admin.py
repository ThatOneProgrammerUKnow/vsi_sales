from django.contrib import admin
from .models import Company, User, Plan, Address, BankDetails

admin.site.register(Company)
admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Address)
admin.site.register(BankDetails)


