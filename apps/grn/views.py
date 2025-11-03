from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from apps.shared.base_views import BaseSessionViewMixin, SingleTableViewBase
from django.views.generic import TemplateView
from .models import GRN, Customer, GoodsItem
from .tables import GRNTable, CustomerTable, GoodsItemTable
from .forms import GRNForm, CustomerForm


def goods(request):
    return render(request, 'grn/goods.html')

class GrnList(SingleTableViewBase, BaseSessionViewMixin, TemplateView):
    template_name = 'grn/grn_list.html'
    menu_slug = 'grn_management'
    model = GRN
    table_class = GRNTable
    paginate_by = 20


class CreateGrnView(BaseSessionViewMixin, CreateView):
    model = GRN
    form_class = GRNForm
    template_name = 'grn/grn_form.html'
    menu_slug = 'grn_management'
    success_url = reverse_lazy('grn:grn_management')


class CustomerList(SingleTableViewBase, BaseSessionViewMixin, TemplateView):
    template_name = 'grn/customer_list.html'
    menu_slug = 'communication_log'
    model = Customer
    table_class = CustomerTable
    paginate_by = 20


class CreateCustomerView(BaseSessionViewMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'grn/customer_form.html'
    menu_slug = 'communication_log'
    success_url = reverse_lazy('grn:customer_management')


class GoodsItemList(SingleTableViewBase, BaseSessionViewMixin, TemplateView):
    template_name = 'grn/goods_list.html'
    menu_slug = 'drive_management'
    model = GoodsItem
    table_class = GoodsItemTable
    paginate_by = 20
