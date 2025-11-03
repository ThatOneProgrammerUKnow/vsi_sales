from django.urls import path
from . import views

app_name  = "grn"

urlpatterns = [
    path('goods', views.goods, name='goods'),
    path('management', views.GrnList.as_view(), name='grn_management'),
    path('new', views.CreateGrnView.as_view(), name='grn_create'),
    path('drive-management', views.GoodsItemList.as_view(), name='drive_management'),
    path('communication-log', views.CustomerList.as_view(), name='communication_log'),
    path('customer-management', views.CustomerList.as_view(), name='customer_management'),
    path('customer/new', views.CreateCustomerView.as_view(), name='customer_create'),
]