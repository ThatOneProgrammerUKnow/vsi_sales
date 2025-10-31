from django.shortcuts import render
from django.views.generic import TemplateView
from apps.shared.base_views import BaseSessionView
from django.contrib.auth.mixins import LoginRequiredMixin


def goods(request):
    return render(request, 'grn/goods.html')

class GrnList(LoginRequiredMixin, BaseSessionView):
    template_name = 'grn/grn_list.html'
    menu_slug = "grn_management"

