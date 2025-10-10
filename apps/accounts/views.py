from allauth.account import views as allauth_views
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse

class LoginView(allauth_views.LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


class SignupView(allauth_views.SignupView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "account/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Dashboard"
        context["page_description"] = "This is a page description"
        context["menu_slug"] = "dashboard"
        return context
