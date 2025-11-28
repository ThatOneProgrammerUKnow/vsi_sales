from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django_tables2 import SingleTableView

from apps.shared.base_views import BaseSessionViewMixin, CustomCreateView
from .models import Client, Product, Invoice, Order, OrderItem, Status
from .tables import ClientTable, ProductTable, InvoiceTable, OrderTable
from .forms import ClientForm, ProductForm, OrderForm, InvoiceForm, StatusForm


#=====# Tables #=====#
#--->>> Client table
class ClientListView(BaseSessionViewMixin, SingleTableView):
    model = Client
    table_class = ClientTable
    template_name = "apps/sales/client_table.html"
    menu_slug = "client"

    def get_queryset(self):
        # Only show clients ders for the logged-in user's company
        return Client.objects.filter(company=self.request.user.company)
    

#--->>> Product table
class ProductListView(BaseSessionViewMixin, SingleTableView):
    model = Product
    table_class = ProductTable
    
    template_name = "apps/sales/product_table.html"
    menu_slug = "product"

    def get_queryset(self):
        # Only show products for the logged-in user's company
        return Product.objects.filter(company=self.request.user.company)
    

#--->>> Order table
class OrderListView(BaseSessionViewMixin, SingleTableView):
    model = Order
    table_class = OrderTable
    template_name = "apps/sales/order_table.html"
    menu_slug = "order"

    def get_queryset(self):
        # Only show orders for the logged-in user's company
        return Order.objects.filter(company=self.request.user.company)

#--->>> Invoice table
class InvoiceListView(BaseSessionViewMixin, SingleTableView):
    model = Invoice
    table_class = InvoiceTable
    template_name = "apps/sales/invoice_table.html"
    menu_slug = "invoice"

    def get_queryset(self):
        # Only show invoices for the logged-in user's company
        return Invoice.objects.filter(order__company=self.request.user.company)

#=====# Create Views #=====#
#--->>> Create Invoice
class CreateInvoiceView(BaseSessionViewMixin, CustomCreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "apps/sales/generic_form.html"
    menu_slug = "invoice"
    title_slug = "Create Invoice"
    button_slug = "Create Invoice"
    cancel_url = reverse_lazy("sales:invoice_table")
    success_url = reverse_lazy("sales:invoice_table")

#--->>> Create Order
class CreateOrderView(BaseSessionViewMixin, CustomCreateView):
    model = Order
    form_class = OrderForm
    template_name = "apps/sales/generic_form.html"
    menu_slug = "order"
    title_slug = "Create Order"
    button_slug = "Create Order"
    cancel_url = reverse_lazy("sales:order_table")
    success_url = reverse_lazy("sales:order_table")

#--->>> Add Product
class AddProductView(BaseSessionViewMixin, CustomCreateView):
    model = Product
    form_class = ProductForm
    template_name = "apps/sales/generic_form.html"
    menu_slug = "product"
    title_slug = "Add Product"
    button_slug = "Add Product"
    cancel_url = reverse_lazy("sales:product_table")
    success_url = reverse_lazy("sales:product_table")

#--->>> Create Client 
class AddClientView(BaseSessionViewMixin, CustomCreateView):
    model = Client
    form_class = ClientForm
    template_name = "apps/sales/generic_form.html"
    menu_slug = "client"
    title_slug = "Add Client"
    button_slug = "Add Client"
    cancel_url = reverse_lazy("sales:client_table")
    success_url = reverse_lazy("sales:client_table")

#--->>> Create Client 
class AddStatusView(BaseSessionViewMixin, CustomCreateView):
    model = Status
    form_class = StatusForm
    template_name = "apps/sales/generic_form.html"
    menu_slug = "order"
    title_slug = "Add Status"
    button_slug = "Add Status"
    cancel_url = reverse_lazy("sales:order_table")
    success_url = reverse_lazy("sales:order_table")

