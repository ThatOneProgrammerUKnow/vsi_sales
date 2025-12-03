from allauth.account import views as allauth_views
from django.contrib.auth import logout
from django.views.generic import CreateView, TemplateView
from apps.shared.base_views import BaseSessionViewMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import Company
from .forms import CreateCompanyForm

#=====# Generic Variables #=====#
generic_form = "generic/generic_form.html"
confirm_delete = "generic/confirm_delete.html"

#==================================================================# User #==================================================================# 
class LoginView(allauth_views.LoginView):
    template_name = "apps/accounts/login.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class SignupView(allauth_views.SignupView):
    template_name = "apps/accounts/signup.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class PasswordResetView(allauth_views.PasswordResetView):
    template_name = "apps/accounts/password_reset.html"

class PasswordResetDoneView(allauth_views.PasswordResetDoneView):
    template_name = "apps/accounts/password_reset_done.html"

class PasswordResetFromKeyView(allauth_views.PasswordResetFromKeyView):
    template_name = "apps/accounts/password_reset_from_key.html"

class PasswordResetFromKeyDoneView(allauth_views.PasswordResetFromKeyDoneView):
    template_name = "apps/accounts/password_reset_from_key_done.html"

class EmailVerificationSentView(allauth_views.EmailVerificationSentView):
    template_name = "apps/accounts/verification_sent.html"

class ConfirmEmailView(allauth_views.ConfirmEmailView):
    template_name = "apps/accounts/email_confirm.html"

#==================================================================# Company #==================================================================#
class CreateCompanyView(BaseSessionViewMixin, CreateView):
    model = Company
    form_class = CreateCompanyForm
    template_name = generic_form
    title_slug = "Create Company"
    button_slug = "Create"
    success_url = reverse_lazy("accounts:dashboard")
    cancel_url = reverse_lazy("accounts:dashboard")


#==================================================================# Dashboard #==================================================================#
class DashboardView(BaseSessionViewMixin, TemplateView):
    template_name = "apps/accounts/dashboard.html"
    menu_slug = "dashboard"

#==================================================================# Function based views #==================================================================#
def logout_view(request):
    """
    Log out the user if they are logged in. Then redirect to the login page.
    """
    logout(request)
    return redirect("accounts:login")

