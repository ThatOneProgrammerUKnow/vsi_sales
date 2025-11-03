from allauth.account import views as allauth_views
from django.contrib.auth import logout
from django.views.generic import TemplateView
from apps.shared.base_views import BaseSessionViewMixin
from django.shortcuts import redirect

class LoginView(allauth_views.LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


class SignupView(allauth_views.SignupView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


class DashboardView(BaseSessionViewMixin, TemplateView):
    template_name = "account/dashboard.html"
    menu_slug = "dashboard"


def logout_view(request):
    """
    Log out the user if they are logged in. Then redirect to the login page.
    """
    logout(request)
    return redirect("account_login")