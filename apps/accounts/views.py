from allauth.account import views as allauth_views
from django.contrib.auth import logout
from django.views.generic import CreateView, TemplateView, ListView, View
from apps.shared.base_views import BaseSessionViewMixin

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden

from .models import Company, CompanyManager, Address, BankDetails, JoinRequest
from .forms import CreateCompanyForm, CompanyAddressForm, CompanyBankingForm, JoinCompany

#=====# Generic Variables #=====#
generic_form = "generic/generic_form.html"
confirm_delete = "generic/confirm_delete.html"

#=====# Console tools #=====#
RED = "\033[31m"
CYAN = "\033[36m]"
RESET = "\033[0m"

ERROR_COLOR = RED

#==================================================================# Custom View Mixins #==================================================================# 
class BaseSessionViewMixin(BaseSessionViewMixin):
    app_name = "accounts"


#==================================================================# User #==================================================================# 
class LoginView(allauth_views.LoginView):
    template_name = "apps/accounts/Authorization/login.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class SignupView(allauth_views.SignupView):
    template_name = "apps/accounts/Authorization/signup.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class PasswordResetView(allauth_views.PasswordResetView):
    template_name = "apps/accounts/Authorization/password_reset.html"

class PasswordResetDoneView(allauth_views.PasswordResetDoneView):
    template_name = "apps/accounts/Authorization/password_reset_done.html"

class PasswordResetFromKeyView(allauth_views.PasswordResetFromKeyView):
    template_name = "apps/accounts/Authorization/password_reset_from_key.html"

class PasswordResetFromKeyDoneView(allauth_views.PasswordResetFromKeyDoneView):
    template_name = "apps/accounts/Authorization/password_reset_from_key_done.html"

class EmailVerificationSentView(allauth_views.EmailVerificationSentView):
    template_name = "apps/accounts/Authorization/verification_sent.html"

class ConfirmEmailView(allauth_views.ConfirmEmailView):
    template_name = "apps/accounts/Authorization/email_confirm.html"

#==================================================================# Company #==================================================================#
#====================# Join company #====================#
'''
Creates "joinrequest" object with fields "company" and "user"
'''
class JoinCompany(BaseSessionViewMixin, CreateView): # Creates "Joinrequest" object
    model = JoinRequest
    form_class = JoinCompany
    template_name = generic_form
    title_slug = "Join Company"
    button_slug = "Request to join"
    cancel_url = reverse_lazy("accounts:dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("accounts:dashboard")

#====================# Join requests | List view #====================#
class JoinRequestView(BaseSessionViewMixin, ListView):
    model = JoinRequest
    template_name = "apps/accounts/join_requests.html"
    menu_slug = "join_requests"
    context_object_name = "joinrequests"


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(company=self.request.user.company)
    
#====================# Approve/Deny request #====================#
class ApproveJoinRequestView(BaseSessionViewMixin, View):
    def post(self, request, pk):
        join_request = get_object_or_404(JoinRequest, pk=pk)

        # Security
        managers = CompanyManager.objects.filter(company=join_request.company)
        m_users = []
        for m in managers: m_users.append(m.user)

        if request.user not in m_users:
            return HttpResponseForbidden("You are not a manager. Acces denied")
        
        # Add user to company
        user = join_request.user
        user.company = join_request.company
        user.save()

        join_request.delete()

        return redirect("accounts:join_requests")
    
class DenyJoinRequestView(BaseSessionViewMixin, View):
    def post(self, request, pk):
        join_request = get_object_or_404(JoinRequest, pk=pk)

        # Security
        managers = CompanyManager.objects.filter(company=join_request.company)
        m_users = []
        for m in managers: m_users.append(m.user)

        if request.user not in m_users:
            return HttpResponseForbidden("You are not a manager. Acces denied")
        

        join_request.delete()

        return redirect("accounts:dashboard")






#====================# Create company #====================#
#=====# General #=====#
class CreateCompanyView(BaseSessionViewMixin, CreateView):
    model = Company
    form_class = CreateCompanyForm
    template_name = generic_form
    title_slug = "Create Company"
    button_slug = "Create"
    cancel_url = reverse_lazy("accounts:dashboard")
    
    
    def form_valid(self, form):
        response = super().form_valid(form) 
        print(f"\nCreating company:")
        print(f"name={self.object.name}")
        print(f"owner={self.request.user.username}\n")
        
        # Assigning user to the company
        user = self.request.user
        user.company = self.object
        user.save()
        

        # Automatically making current user manager of company
        CompanyManager.objects.create(
            user = self.request.user,
            company=self.object
        )


        return response

    def get_success_url(self):
        return reverse(
            "accounts:add_company_address",
            kwargs={"company_id": self.object.id}
        )

#=====# Address #=====#
class CompanyAddressView(BaseSessionViewMixin, CreateView):
    model = Address
    form_class = CompanyAddressForm
    template_name = generic_form
    title_slug = "Add Company Address"
    button_slug = "Add Address"
    button2_slug = "Skip Address"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, id=self.kwargs['company_id'])
        context['company'] = company

        context['cancel_url'] = reverse("accounts:add_company_banking", kwargs={"company_id" : self.kwargs["company_id"]})

        return context

    def form_valid(self, form):
        company = get_object_or_404(Company, id=self.kwargs['company_id'])
        form.instance.company = company
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'accounts:add_company_banking', 
            kwargs={'company_id': self.kwargs['company_id']}
            )

#=====# Banking #=====#
class CompanyBankingView(BaseSessionViewMixin, CreateView):
    model = BankDetails
    form_class = CompanyBankingForm
    template_name = generic_form
    title_slug = "Add Company Banking Details"
    button_slug = "Add Banking Details"
    button2_slug = "Skip Banking"
    cancel_url = reverse_lazy("accounts:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, id=self.kwargs['company_id'])
        context['company'] = company
        
        return context

    def form_valid(self, form):
        company = get_object_or_404(Company, id=self.kwargs['company_id'])
        form.instance.company = company
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("accounts:dashboard")



#==================================================================# Template #==================================================================#
#====================# Template views #====================#
# Dashboard
'''
Send "manager" context to the template
'''
class DashboardView(BaseSessionViewMixin, TemplateView):
    template_name = "apps/accounts/dashboard.html"
    menu_slug = "dashboard"

    def get_context_data(self):
        context = super().get_context_data()

        user = self.request.user
        context["manager"] = CompanyManager.objects.filter(user=user, company=user.company).exists # Is the user a manager? Boolean

        return context
    
#====================# List views #====================#
# Company information

# Staff


    

#==================================================================# Function based views #==================================================================#
def logout_view(request):
    """
    Log out the user if they are logged in. Then redirect to the login page.
    """
    logout(request)
    return redirect("accounts:login")

