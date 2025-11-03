import django_tables2 as tables
from django.conf import settings
from .models import GRN, Customer, GoodsItem


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


class GoodsItemTable(tables.Table):
    grn_number = tables.Column(accessor="grn__grn_number")
    customer_name = tables.Column(accessor="grn__customer__name")

    class Meta:
        model = GoodsItem
        exclude = ("id", "updated_at", "credit_request_reason")
