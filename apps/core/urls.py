"""
╔══════════════════════════════════════════════════════════╗
║  CORE APP URL ROUTING                                    ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/apps/core/urls.py                  ║
║  PASKIRTIS: Visi core app URL patterns                  ║
╚══════════════════════════════════════════════════════════╝
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import payment_views  # ← PRIDĖTA

urlpatterns = [
    # ═══════════════════════════════════════════════════════
    # PAGRINDINIS PUSLAPIS
    # ═══════════════════════════════════════════════════════
    path('', views.index, name='index'),

    # ═══════════════════════════════════════════════════════
    # AUTHENTICATION
    # ═══════════════════════════════════════════════════════
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ═══════════════════════════════════════════════════════
    # PASSWORD RESET
    # ═══════════════════════════════════════════════════════
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='core/password_reset.html',
             email_template_name='core/password_reset_email.html',
             subject_template_name='core/password_reset_subject.txt',
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='core/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='core/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='core/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # ═══════════════════════════════════════════════════════
    # DASHBOARD
    # ═══════════════════════════════════════════════════════
    path('dashboard/', views.dashboard, name='dashboard'),

    # ═══════════════════════════════════════════════════════
    # VIN SEARCH & REPORTS
    # ═══════════════════════════════════════════════════════
    path('api/search-vin/', views.search_vin, name='search_vin'),
    path('report/<int:report_id>/', views.view_report, name='view_report'),

    # ═══════════════════════════════════════════════════════
    # PAYMENT & CREDITS (STRIPE) ← NAUJAS SKYRIUS
    # ═══════════════════════════════════════════════════════
    path('buy-credits/', payment_views.buy_credits, name='buy_credits'),
    path('create-checkout-session/', payment_views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/', payment_views.payment_success, name='payment_success'),
    path('payment-cancel/', payment_views.payment_cancel, name='payment_cancel'),
    path('stripe-webhook/', payment_views.stripe_webhook, name='stripe_webhook'),

    # Stripe Webhook
    path('webhook/stripe/', payment_views.stripe_webhook, name='stripe_webhook'),

    # ═══════════════════════════════════════════════════════
    # FUNDS (OLD - OPTIONAL, galima ištrinti jei naudosite tik Stripe)
    # ═══════════════════════════════════════════════════════
    path('add-funds/', views.add_funds, name='add_funds'),

    # ═══════════════════════════════════════════════════════
    # PAGES
    # ═══════════════════════════════════════════════════════
    path('pricing/', views.pricing, name='pricing'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),

    # ═══════════════════════════════════════════════════════
    # API ENDPOINTS
    # ═══════════════════════════════════════════════════════
    path('api/balance/', views.api_balance, name='api_balance'),
    path('api/recent-reports/', views.api_recent_reports, name='api_recent_reports'),
]
