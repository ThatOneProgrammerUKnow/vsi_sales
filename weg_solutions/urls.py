"""
URL configuration for weg_solutions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from apps.accounts.views import LoginView, SignupView, DashboardView, logout_view

urlpatterns = [
    path("",
        RedirectView.as_view(pattern_name="account_login"),
        name="root-redirect",
    ),
    # Override allauth views
    path("accounts/logout/", logout_view, name="account_logout"),
    path("accounts/login/", LoginView.as_view(), name="account_login"),
    path("accounts/signup/", SignupView.as_view(), name="account_signup"),
    path("accounts/", include("allauth.urls")),
    path(
        "admin/login/",
        RedirectView.as_view(pattern_name="account_login"),
        name="redirect-to-login",
    ),
    path("admin/", admin.site.urls),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("grn/", include("apps.grn.urls", namespace="grn")),
]
