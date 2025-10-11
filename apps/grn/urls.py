from django.urls import path
from . import views

app_name  = "grn"

urlpatterns = [
    path('goods_table', views.goods_table, name='goods_table'),
]