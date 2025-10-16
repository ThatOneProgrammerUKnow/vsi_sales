from django.urls import path
from . import views

app_name  = "grn"

urlpatterns = [
    path('goods', views.goods, name='goods'),
]