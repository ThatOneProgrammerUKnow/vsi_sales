import django_tables2 as tables
from django.conf import settings
from .models import GRN, Customer


class GRNTable(tables.Table):
    customer_name = tables.Column(accessor="customer__name")
    customer_branch = tables.Column(accessor="customer__branch")


    class Meta:
        model = GRN
        exclude = ("id", "updated_at")


class CustomerTable(tables.Table):
    class Meta:
        model = Customer
        exclude = ("id", "updated_at")
