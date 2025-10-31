from allauth.account import views as allauth_views
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.shared.base_views import BaseSessionView

class LoginView(allauth_views.LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


class SignupView(allauth_views.SignupView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


class DashboardView(LoginRequiredMixin, BaseSessionView):
    template_name = "account/dashboard.html"
    menu_slug = "dashboard"
