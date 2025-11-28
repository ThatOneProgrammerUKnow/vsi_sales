from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    #===# Clients #===#
    path("clients/", views.ClientListView.as_view(), name="client_table"),
    path("clients/add", views.AddClientView.as_view(), name="add_client"),

    #===# Products #===#
    path("products/", views.ProductListView.as_view(), name="product_table"),
    path("product/add", views.AddProductView.as_view(), name="add_product"),

    #===# Orders #===#
    path("orders/", views.OrderListView.as_view(), name="order_table"),
    path("order/create", views.CreateOrderView.as_view(), name="create_order"),

    #===# Invoice #===#
    path("invoice/", views.InvoiceListView.as_view(), name="invoice_table"),
    path("invoice/create", views.CreateInvoiceView.as_view(), name="create_invoice"),
]