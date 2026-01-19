#===================================# Django Imports #===================================#
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.views import View
from django_tables2 import SingleTableView
from django_tables2.config import RequestConfig
from django.http import Http404, HttpResponse
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.conf import settings

#===================================# Python  #===================================#
from pathlib import Path

#===================================# Custom #===================================#

from apps.shared.base_views import BaseSessionViewMixin, CustomCreateView, CompanyFilterUpdateMixin, CompanyFilterDeleteMixin
from apps.shared.helper_methods import discount

#===================================# App models, forms & Tables #===================================#

from .models import Client, Product, Invoice, Order, OrderItem, Status
from .tables import ClientTable, ProductTable, InvoiceTable, OrderTable
from .forms import ClientForm, ProductForm, OrderForm, InvoiceForm, StatusForm, OrderItemFormSet

#===================================# Third party #===================================#
from playwright.sync_api import sync_playwright

#=====# Generic Variables #=====#
generic_form = "generic/generic_form.html"
confirm_delete = "generic/confirm_delete.html"
#===============================================================# Tables #===============================================================#
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_modal"] = "False"
        return context

#--->>> Invoice table
class InvoiceListView(BaseSessionViewMixin, SingleTableView):
    model = Invoice
    table_class = InvoiceTable
    template_name = "apps/sales/invoice_table.html"
    menu_slug = "invoice"

    def get_queryset(self):
        # Only show invoices for the logged-in user's company
        return Invoice.objects.filter(order__company=self.request.user.company)

#===============================================================# Create Views #===============================================================#
#--->>> Create Invoice
class CreateInvoiceView(BaseSessionViewMixin, CustomCreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = generic_form
    menu_slug = "invoice"
    title_slug = "Create Invoice"
    button_slug = "Create Invoice"
    cancel_url = reverse_lazy("sales:invoice_table")
    success_url = reverse_lazy("sales:invoice_table")

    def form_valid(self, form):
        order_pk = self.kwargs["on"]
        order = get_object_or_404(Order, pk=order_pk)

        # Filter to company
        if order.company != self.request.user.company:
            raise Http404("Order not found")


        self.object = form.save(commit=False)
        self.object.order = order
        self.object.save()

        return super().form_valid(form)

#--->>> Create Order with Items (uses inline formset)
class CreateOrderView(BaseSessionViewMixin, CustomCreateView):
    model = Order
    form_class = OrderForm
    template_name = generic_form
    menu_slug = "order"
    title_slug = "Create Order"
    heading2_slug = "Products"
    button_slug = "Create Order"
    button2_slug = "Add product"
    cancel_url = reverse_lazy("sales:order_table")
    success_url = reverse_lazy("sales:order_table")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST, instance=self.object, form_kwargs={'user': self.request.user})
        else:
            context['formset'] = OrderItemFormSet(instance=self.object, form_kwargs={'user': self.request.user})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.company = self.request.user.company
            self.object.save()
            
            formset.instance = self.object
            items = formset.save(commit=False)

        
            for item in items:
                # Store unit price at order (use product price excluding VAT)
                price = item.product.price_before_vat
                item.price_at_checkout = discount(price, item.discount) 
                item.save()
            
            return redirect(self.success_url)  
        else:
            return self.form_invalid(form)

#--->>> Add Product
class AddProductView(BaseSessionViewMixin, CustomCreateView):
    model = Product
    form_class = ProductForm
    template_name = generic_form
    menu_slug = "product"
    title_slug = "Add Product"
    button_slug = "Add Product"
    cancel_url = reverse_lazy("sales:product_table")
    success_url = reverse_lazy("sales:product_table")


#--->>> Create Client 
class AddClientView(BaseSessionViewMixin, CustomCreateView):
    model = Client
    form_class = ClientForm
    template_name = generic_form
    menu_slug = "client"
    title_slug = "Add Client"
    button_slug = "Add Client"
    cancel_url = reverse_lazy("sales:client_table")
    success_url = reverse_lazy("sales:client_table")

#--->>> Create Client 
class AddStatusView(BaseSessionViewMixin, CustomCreateView):
    model = Status
    form_class = StatusForm
    template_name = generic_form
    menu_slug = "order"
    title_slug = "Add Status"
    button_slug = "Add Status"
    cancel_url = reverse_lazy("sales:order_table")
    success_url = reverse_lazy("sales:order_table")




#===============================================================# Delete Views #===============================================================#
#--->>> Delete Product
class DeleteProductView(BaseSessionViewMixin, CompanyFilterDeleteMixin):
    model = Product
    template_name = confirm_delete
    success_url = reverse_lazy("sales:product_table")
    cancel_url = reverse_lazy("sales:product_table")

#--->>> Delete Client
class DeleteClientView(BaseSessionViewMixin, CompanyFilterDeleteMixin):
    model = Client
    template_name = confirm_delete
    success_url = reverse_lazy("sales:client_table")
    cancel_url = reverse_lazy("sales:client_table")

#--->>> Delete Order
class DeleteOrderView(BaseSessionViewMixin, CompanyFilterDeleteMixin):
    model = Order
    template_name = confirm_delete
    success_url = reverse_lazy("sales:order_table")
    cancel_url = reverse_lazy("sales:order_table")

#--->>> Delete OrderItem
class DeleteOrderItemView(BaseSessionViewMixin, DeleteView):
    model = OrderItem
    template_name = confirm_delete
    def get_success_url(self):
        order_pk = self.object.order.pk   # assuming OrderItem has FK: order
        return reverse("sales:expand_order", kwargs={"pk": order_pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_pk = self.object.order.pk
        context["cancel_url"] = reverse("sales:expand_order", kwargs={"pk": order_pk})
        return context

#--->>> Delete Invoice
class DeleteInvoiceView(BaseSessionViewMixin, DeleteView):
    model = Invoice
    template_name = confirm_delete
    success_url = reverse_lazy("sales:invoice_table")
    cancel_url = reverse_lazy("sales:invoice_table")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.order.company == self.request.user.company: 
            raise Http404("You are not authorized to delete this object.")
        return obj

#--->>> Delete Status
class DeleteStatusView(BaseSessionViewMixin, CompanyFilterDeleteMixin):
    model = Status
    template_name = confirm_delete
    success_url = reverse_lazy("sales:order_table")
    cancel_url = reverse_lazy("sales:order_table")

#===============================================================# Update Views #===============================================================#
#--->>> Update Product
class UpdateProductView(BaseSessionViewMixin, CompanyFilterUpdateMixin):
    model = Product
    template_name = generic_form
    success_url = reverse_lazy("sales:product_table")
    cancel_url = reverse_lazy("sales:product_table")
    form_class = ProductForm
    title_slug = "Update Product"
    button_slug = "Update"


#--->>> Update Client
class UpdateClientView(BaseSessionViewMixin, CompanyFilterUpdateMixin):
    model = Client
    template_name = generic_form
    success_url = reverse_lazy("sales:client_table")
    cancel_url = reverse_lazy("sales:client_table")
    form_class = ClientForm
    title_slug = "Update Client"
    button_slug = "Update"

#--->>> Update Order
class UpdateOrderView(BaseSessionViewMixin, CompanyFilterUpdateMixin):
    model = Order
    template_name = generic_form
    success_url = reverse_lazy("sales:order_table")
    cancel_url = reverse_lazy("sales:order_table")
    form_class = OrderForm
    title_slug = "Update Order"
    button_slug = "Update"
    button2_slug = "Add Product"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST, instance=self.object, form_kwargs={'user': self.request.user})
        else:
            context['formset'] = OrderItemFormSet(instance=self.object, form_kwargs={'user': self.request.user})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.company = self.request.user.company
            self.object.save()
            
            formset.instance = self.object
            items = formset.save(commit=False)

            if self.object.client.vat_verified == False:
                for item in items:
                    # Store unit price at order (use product price including VAT)
                    item.price_at_checkout = item.product.price_after_vat
                    item.save()
            else:
                for item in items:
                    # Store unit price at order (use product price excluding VAT)
                    item.price_at_checkout = item.product.price_before_vat
                    item.save()
            
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


#--->>> Update Invoice
class UpdateInvoiceView(BaseSessionViewMixin, CompanyFilterUpdateMixin):
    model = Invoice
    template_name = generic_form
    success_url = reverse_lazy("sales:invoice_table")
    cancel_url = reverse_lazy("sales:invoice_table")
    form_class = InvoiceForm
    title_slug = "Update Invoice"
    button_slug = "Update"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(order__company=self.request.user.company)

#--->>> Update Status
class UpdateStatusView(BaseSessionViewMixin, CompanyFilterUpdateMixin):
    model = Status
    template_name = generic_form
    success_url = reverse_lazy("sales:order_table")
    cancel_url = reverse_lazy("sales:order_table")
    form_class = StatusForm
    title_slug = "Update Status"
    button_slug = "Update"

#===============================================================# Modal Views #===============================================================#
class ExpandView(BaseSessionViewMixin, DetailView):
    model = Order
    template_name = "apps/sales/order_table.html"
    menu_slug = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_items = OrderItem.objects.filter(order=self.object)
        context["order_items"] = order_items

        # Calculate total order price
        total = sum((item.price_at_checkout * item.qty) for item in order_items)
        context["total_price"] = total
        context["show_modal"] = "True"

        # Also render the orders table on the detail page
        queryset = Order.objects.filter(company=self.request.user.company)
        table = OrderTable(queryset)
        RequestConfig(self.request).configure(table)
        context["table"] = table
        return context
    
class PreviewInvoiceView(BaseSessionViewMixin, DetailView):
    model = Invoice
    template_name = "apps/sales/invoice.html"
    menu_slug = "invoice"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        invoice_items = OrderItem.objects.filter(order=self.object.order)

        for item in invoice_items:
            item.line_total = item.qty*item.price_at_checkout

        context["invoice_items"] = invoice_items
        context["company"] = self.request.user.company
        context["email"] = self.request.user.email
        return context
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.order.company != self.request.user.company:
            raise Http404("Invoice not found")
        
        return obj

class GenerateInvoicePDFView(PreviewInvoiceView):
    def get(self, request, *args, **kwargs):
        # Get invoice object & context
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # Render HTML template to string
        html_content = render_to_string('apps/sales/invoice_standalone.html', context)

        # Generate PDF with Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Set the content of the page
            page.set_content(html_content, wait_until="networkidle")
            
            pdf_bytes = page.pdf(format="A4", print_background=True)
            browser.close()

        # Return PDF as response
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="invoice_{self.object.id}.pdf"'
        return response

