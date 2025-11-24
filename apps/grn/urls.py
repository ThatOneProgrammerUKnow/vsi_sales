from django.urls import path
from . import views

app_name  = "grn"

urlpatterns = [
    # Grns
    path('management/', views.GrnList.as_view(), name='grn_management'),
    path('new/', views.CreateGrnView.as_view(), name='grn_create'),
    path('delete/', views.DeleteGrn.as_view(), name='grn_delete'),

    # Goods
    path('goods/', views.GoodsItemList.as_view(), name='goods'),
    path('goods/<int:goods_item_id>/', views.ExpandGoods.as_view(), name='expand_good'),
    path('goods/<int:pk>/delete/', views.DeleteGoodsItem.as_view(), name='delete_goods_item'),

    # Customer
    path('customer-management/', views.CustomerList.as_view(), name='customer_management'),
    path('customer/new/', views.CreateCustomerView.as_view(), name='customer_create'),
    path('customer/<int:pk>/delete/', views.DeleteCustomer.as_view(), name='delete_customer'),

    # Contact Persons
    path('contact_persons/<int:customer_id>/', views.ContactPersonList.as_view(), name='contact_persons'),
    path('contact_person', views.AddContactPerson.as_view(), name="add_contact_person"),
    path('contact-person/<int:pk>/delete/', views.DeleteContactPerson.as_view(), name='delete_contact_person'),
    
]