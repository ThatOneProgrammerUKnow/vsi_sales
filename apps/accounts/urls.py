from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    #========================================================# Users #========================================================#  
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),

    #=====# Django Authentication #=====# 
    path('password/reset/', views.PasswordResetView.as_view(), name='account_reset_password'),
    path('password/reset/done/', views.PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    path('password/reset/key/<uidb36>-<key>/', views.PasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
    path('password/reset/key/done/', views.PasswordResetFromKeyDoneView.as_view(), name='account_reset_password_from_key_done'),
    path('confirm-email/', views.EmailVerificationSentView.as_view(), name='account_email_verification_sent'),
    path('confirm-email/<key>/', views.ConfirmEmailView.as_view(), name='account_confirm_email'),

    #========================================================# Company #========================================================#  
    path('company/create', views.CreateCompanyView.as_view(), name='create_company'),
    path('company/add_address/<int:company_id>', views.CompanyAddressView.as_view(), name='add_company_address'),
    path('company/add_banking/<int:company_id>', views.CompanyBankingView.as_view(), name='add_company_banking'),

    #========================================================# Dashboard #========================================================#  
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    
]
