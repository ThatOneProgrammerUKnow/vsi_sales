from django.urls import path
from . import views

app_name  = "grn"

urlpatterns = [
    path('goods', views.goods, name='goods'),
    path('grn-management', views.GrnList.as_view(), name='grn_management'),
    path('drive-management', views.GrnList.as_view(), name='drive_management'),
    path('communication-log', views.GrnList.as_view(), name='communication_log'),
]