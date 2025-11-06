"""
VIEWS (KONTROLERIAI)
Čia visi puslapių kontroleriai ir logika
✅ UPDATED: Dabar išsaugo ir rodo HTML iš CheapCarfax API
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from decimal import Decimal
import json
import logging

from .models import Report, Transaction, UserProfile
from .forms import RegistrationForm, LoginForm, VINSearchForm, AddFundsForm, ContactForm
from .api import fetch_vehicle_report

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════
# PAGRINDINIS PUSLAPIS
# ═══════════════════════════════════════════════════════

def index(request):
    """
    Pagrindinis puslapis
    Rodo: Hero sekcija, pricing, FAQ
    """
    context = {
        'prices': settings.REPORT_PRICES,
    }
    return render(request, 'core/index.html', context)


# ═══════════════════════════════════════════════════════
# AUTENTIFIKACIJA
# ═══════════════════════════════════════════════════════

def register_view(request):
    """
    Registracijos puslapis
    GET: Rodo formą
    POST: Sukuria naują user
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatiškai prisijungti po registracijos
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to AutoInfo.')
            return redirect('dashboard')
    else:
        form = RegistrationForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    """
    Prisijungimo puslapis
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                remember_me = form.cleaned_data.get('remember_me')

                # Handle Remember Me functionality
                if remember_me:
                    # Keep session for 30 days when Remember Me is checked
                    request.session.set_expiry(2592000)  # 30 days in seconds
                else:
                    # Session expires when browser closes
                    request.session.set_expiry(0)

                messages.success(request, f'Welcome back!')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})


@login_required
def logout_view(request):
    """Atsijungimas"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


# ═══════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════

@login_required
def dashboard(request):
    """
    Vartotojo dashboard
    Rodo: balansą, VIN paieškos formą, ataskaitas
    """
    # Gauti vartotojo ataskaitas (paskutines 10)
    reports = Report.objects.filter(user=request.user).order_by('-created_at')[:10]

    # VIN paieškos forma
    search_form = VINSearchForm()

    # Statistika
    total_reports = Report.objects.filter(user=request.user).count()

    context = {
        'reports': reports,
        'form': search_form,
        'total_reports': total_reports,
        'prices': settings.REPORT_PRICES,
    }
    return render(request, 'core/dashboard.html', context)


# ═══════════════════════════════════════════════════════
# VIN PAIEŠKA IR ATASKAITOS
# ═══════════════════════════════════════════════════════

@login_required
@require_http_methods(["POST"])
def search_vin(request):
    """
    VIN paieška ir reporto generavimas
    ✅ UPDATED: Dabar išsaugo HTML iš CheapCarfax API
    AJAX endpoint - grąžina JSON
    """
    try:
        data = json.loads(request.body)
        vin = data.get('vin', '').upper()
        report_type = data.get('reportType', 'carfax')

        # Validacija
        if len(vin) != 17:
            return JsonResponse({
                'success': False,
                'message': 'Invalid VIN format. VIN must be 17 characters.'
            }, status=400)

        # Gauti kainą
        prices = settings.REPORT_PRICES.get(report_type, {})
        price = Decimal(str(prices.get('single', 0)))

        # Patikrinti balansą
        profile = request.user.profile
        if not profile.has_sufficient_balance(price):
            return JsonResponse({
                'success': False,
                'message': f'Insufficient balance. You need {price} PLN. Please add funds.'
            }, status=400)

        # ✅ Gauti ataskaitą iš API (SU HTML!)
        logger.info(f"Fetching {report_type} report for VIN: {vin}")
        report_data = fetch_vehicle_report(vin, report_type)

        if not report_data:
            return JsonResponse({
                'success': False,
                'message': 'Could not retrieve report. Please try again later.'
            }, status=500)

        # Nuskaičiuoti balansą
        profile.deduct_balance(price)
        logger.info(f"Deducted {price} PLN from {request.user.username}")

        # ✅ Išsaugoti ataskaitą SU HTML!
        report = Report.objects.create(
            user=request.user,
            vin=vin,
            report_type=report_type,
            report_data=report_data,  # JSON duomenys
            report_html=report_data.get('html', ''),  # ✅ HTML iš CheapCarfax!
            price_paid=price,
            score=report_data.get('score', 0),
            accidents=report_data.get('accidents', 0),
            owners=report_data.get('owners', 0)
        )

        logger.info(f"Report created: ID={report.id}, VIN={vin}, Has HTML={report.has_html}")

        return JsonResponse({
            'success': True,
            'report': {
                'id': report.id,
                'vin': report.vin,
                'type': report.get_report_type_display(),
                'score': report.score,
                'accidents': report.accidents,
                'owners': report.owners,
                'price': float(price),
                'has_html': report.has_html,  # ✅ Info ar yra HTML
                'created_at': report.created_at.strftime('%Y-%m-%d %H:%M')
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request format.'
        }, status=400)
    except Exception as e:
        logger.error(f"Search VIN error: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)


@login_required
def view_report(request, report_id):
    """
    Peržiūrėti konkrečią ataskaitą
    ✅ UPDATED: Dabar perduoda HTML į template
    """
    report = get_object_or_404(Report, id=report_id, user=request.user)

    logger.info(f"Viewing report: ID={report.id}, VIN={report.vin}, Has HTML={report.has_html}")

    context = {
        'report': report,
    }
    return render(request, 'core/view_report.html', context)


# ═══════════════════════════════════════════════════════
# PINIGŲ ĮKĖLIMAS
# ═══════════════════════════════════════════════════════

@login_required
def add_funds(request):
    """
    Pinigų įkėlimo puslapis
    Development: tiesiog prideda pinigus
    Production: integruoti tikrą payment gateway
    """
    if request.method == 'POST':
        form = AddFundsForm(request.POST)
        if form.is_valid():
            amount = form.get_amount()
            payment_method = form.cleaned_data.get('payment_method')

            # Sukurti transakciją
            import uuid
            transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                currency='PLN',
                payment_method=payment_method,
                transaction_id=str(uuid.uuid4()),
                description=f'Account top-up: {amount} PLN'
            )

            # DEMO MODE: automatiškai mark as completed
            if settings.DEBUG:
                transaction.mark_completed()
                messages.success(request, f'Successfully added {amount} PLN!')
                return redirect('dashboard')

            # Production: redirect to payment gateway
            # return redirect('payment_gateway', transaction_id=transaction.id)
    else:
        form = AddFundsForm()

    context = {'form': form}
    return render(request, 'core/add_funds.html', context)


# ═══════════════════════════════════════════════════════
# KITI PUSLAPIAI
# ═══════════════════════════════════════════════════════

def pricing(request):
    """Kainodaros puslapis"""
    context = {'prices': settings.REPORT_PRICES}
    return render(request, 'core/pricing.html', context)


def faq(request):
    """FAQ puslapis"""
    return render(request, 'core/faq.html')


def contact(request):
    """Kontaktų puslapis"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # TODO: Siųsti email
            messages.success(request, 'Thank you! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})


def terms(request):
    """Terms of Service"""
    return render(request, 'core/terms.html')


def privacy(request):
    """Privacy Policy"""
    return render(request, 'core/privacy.html')


def activation_instructions(request):
    """Activation instructions page"""
    return render(request, 'core/activation_instructions.html')


# ═══════════════════════════════════════════════════════
# API ENDPOINTS (JSON)
# ═══════════════════════════════════════════════════════

@login_required
def api_balance(request):
    """Gauti dabartinį balansą (JSON)"""
    profile = request.user.profile
    return JsonResponse({
        'balance': float(profile.balance),
        'currency': 'PLN'
    })


@login_required
def api_recent_reports(request):
    """Gauti paskutines ataskaitas (JSON)"""
    limit = int(request.GET.get('limit', 10))
    reports = Report.objects.filter(user=request.user).order_by('-created_at')[:limit]

    data = [{
        'id': r.id,
        'vin': r.vin,
        'type': r.get_report_type_display(),
        'score': r.score,
        'price': float(r.price_paid),
        'has_html': r.has_html,  # ✅ Info ar yra HTML
        'created_at': r.created_at.isoformat()
    } for r in reports]

    return JsonResponse({'reports': data})
