from django.urls import path
from . import views

app_name  = "grn"

urlpatterns = [
    path('management', views.GrnList.as_view(), name='grn_management'),
    path('new', views.CreateGrnView.as_view(), name='grn_create'),
    path('goods', views.GoodsItemList.as_view(), name='goods'),
    path('communication-log', views.CustomerList.as_view(), name='communication_log'),
    path('customer-management', views.CustomerList.as_view(), name='customer_management'),
    path('customer/new', views.CreateCustomerView.as_view(), name='customer_create'),
]