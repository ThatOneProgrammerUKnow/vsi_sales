from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    #=======================================# Clients #=======================================#
    path("clients/", views.ClientListView.as_view(), name="client_table"),
    path("clients/add", views.AddClientView.as_view(), name="add_client"),
    path("clients/delete/<int:pk>", views.DeleteClientView.as_view(), name="delete_client"),
    path("clients/update/<int:pk>", views.UpdateClientView.as_view(), name="update_client"),

    #=======================================# Products #=======================================#
    path("products/", views.ProductListView.as_view(), name="product_table"),
    path("product/add", views.AddProductView.as_view(), name="add_product"),
    path("product/delete/<str:pk>", views.DeleteProductView.as_view(), name="delete_product"),
    path("product/update/<str:pk>", views.UpdateProductView.as_view(), name="update_product"),

    #=======================================# Orders #=======================================#
    path("orders/", views.OrderListView.as_view(), name="order_table"),
    path("order/create", views.CreateOrderView.as_view(), name="create_order"),
    path("order/delete/<str:pk>", views.DeleteOrderView.as_view(), name="delete_order"),
    path("order/update/<str:pk>", views.UpdateOrderView.as_view(), name="update_order"),

    #=======================================# Status #=======================================#
    path("order/status/create", views.AddStatusView.as_view(), name="add_status"),
    path("status/delete/<int:pk>", views.DeleteStatusView.as_view(), name="delete_status"),
    path("status/update/<int:pk>", views.UpdateStatusView.as_view(), name="update_status"),

    #=======================================# Invoice #=======================================#
    path("invoice/", views.InvoiceListView.as_view(), name="invoice_table"),
    path("invoice/create/<str:on>/", views.CreateInvoiceView.as_view(), name="create_invoice"),
    path("invoice/delete/<str:pk>", views.DeleteInvoiceView.as_view(), name="delete_invoice"),
    path("invoice/update/<str:pk>", views.UpdateInvoiceView.as_view(), name="update_invoice"),
    path("invoice/preview/<str:pk>", views.PreviewInvoiceView.as_view(), name="preview_invoice"),

    #=======================================# Order Item #=======================================#
    path("order/expand/<str:pk>", views.ExpandView.as_view(), name="expand_order"),
    path("orderitem/delete/<str:pk>", views.DeleteOrderItemView.as_view(), name="delete_orderitem"),
]