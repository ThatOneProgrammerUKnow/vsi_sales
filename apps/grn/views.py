from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from apps.shared.base_views import BaseSessionViewMixin, SingleTableViewBase
from django.views.generic import TemplateView
from django.views import View

from .models import GRN, Customer, GoodsItem
from .tables import GRNTable, CustomerTable, GoodsItemTable
from .forms import GRNForm, CustomerForm, GoodsFormset

#=====# Class based views #=====#
#===# Grn management #===#
## Display grn
class GrnList(SingleTableViewBase, BaseSessionViewMixin, TemplateView):
    template_name = 'grn/grn_list.html'
    menu_slug = 'grn_management'
    model = GRN
    table_class = GRNTable
    paginate_by = 20

## Create grn
class CreateGrnView(BaseSessionViewMixin, CreateView):
    model = GRN
    form_class = GRNForm
    template_name = 'grn/grn_form.html'
    menu_slug = 'grn_management'
    success_url = reverse_lazy('grn:grn_management')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        if self.request.POST:
            data['formset'] = GoodsFormset(self.request.POST, instance=self.object)
        else:
            data['formset'] = GoodsFormset(instance=self.object)
        
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

## Deleting grn
class DeleteGrn(View):
    def get(self, request):
        selected_grns = request.GET.getlist("select")

        context = {
            "selected_grns": selected_grns
        }
        return render(request, "grn/confirm_delete.html", context)

    def post(self, request):
        selected_grns = request.POST.getlist("select")
        if "confirm" in request.POST:
            GRN.objects.filter(pk__in=selected_grns).delete()

        return redirect("grn:grn_management")

        
#===# Customers #===#
class CustomerList(SingleTableViewBase, BaseSessionViewMixin, TemplateView):
    template_name = 'grn/customer_list.html'
    menu_slug = 'customer'
    model = Customer
    table_class = CustomerTable
    paginate_by = 20


class CreateCustomerView(BaseSessionViewMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'grn/customer_form.html'
    menu_slug = 'communication_log'
    success_url = reverse_lazy('grn:customer_management')

#===# Goods #===#
class GoodsItemList(SingleTableViewBase, BaseSessionViewMixin, TemplateView):
    template_name = 'grn/goods.html'
    menu_slug = 'goods'
    model = GoodsItem
    table_class = GoodsItemTable
    paginate_by = 20

#===# Function based views #===#
def goods(request):
    return render(request, 'grn/goods.html')

