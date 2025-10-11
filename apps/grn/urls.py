from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('goods_table', views.goods_table, name='goods_table'),
]