from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from apps.shared.base_views import BaseSessionViewMixin, SingleTableViewBase
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import GRN, Customer
from .tables import GRNTable, CustomerTable
from .forms import GRNForm, CustomerForm


def goods(request):
    return render(request, 'grn/goods.html')

class GrnList(LoginRequiredMixin, SingleTableViewBase, BaseSessionViewMixin, TemplateView):
    template_name = 'grn/grn_list.html'
    menu_slug = 'grn_management'
    model = GRN
    table_class = GRNTable
    paginate_by = 20


class CreateGrnView(LoginRequiredMixin, BaseSessionViewMixin, CreateView):
    model = GRN
    form_class = GRNForm
    template_name = 'grn/grn_form.html'
    menu_slug = 'grn_management'
    success_url = reverse_lazy('grn:grn_management')


class CustomerList(LoginRequiredMixin, SingleTableViewBase, BaseSessionViewMixin, TemplateView):
    template_name = 'grn/customer_list.html'
    menu_slug = 'communication_log'
    model = Customer
    table_class = CustomerTable
    paginate_by = 20


class CreateCustomerView(LoginRequiredMixin, BaseSessionViewMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'grn/customer_form.html'
    menu_slug = 'communication_log'
    success_url = reverse_lazy('grn:customer_management')

