"""
╔══════════════════════════════════════════════════════════╗
║  PAYMENT VIEWS                                           ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/apps/core/payment_views.py         ║
║  PASKIRTIS: Mokėjimų puslapiai ir Stripe integracija    ║
╚══════════════════════════════════════════════════════════╝
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib import messages
import stripe
import json

# Stripe konfigūracija
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def buy_credits(request):
    """
    Kreditų pirkimo puslapis
    Rodo visus galimus paketus (Carfax, Autocheck, NMVTIS)
    """
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'prices': settings.REPORT_PRICES,
    }
    return render(request, 'core/buy_credits.html', context)


@login_required
@require_http_methods(["POST"])
def create_checkout_session(request):
    """
    Sukurti Stripe Checkout sesiją
    Priima: report_type, quantity, amount
    Grąžina: session ID arba error
    """
    try:
        # Parse request body
        data = json.loads(request.body)
        report_type = data.get('report_type')
        quantity = int(data.get('quantity', 1))
        amount = float(data.get('amount'))

        # Validacija
        if report_type not in ['carfax', 'autocheck', 'nmvtis']:
            return JsonResponse({'error': 'Invalid report type'}, status=400)

        if quantity not in [1, 10, 100]:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)

        # Sukurti Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'unit_amount': int(amount * 100),  # Stripe naudoja centus
                    'product_data': {
                        'name': f'{report_type.upper()} Report Package',
                        'description': f'{quantity} {report_type.upper()} report(s)',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/payment-success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/buy-credits/'),
            client_reference_id=str(request.user.id),
            metadata={
                'user_id': request.user.id,
                'report_type': report_type,
                'quantity': quantity,
            }
        )

        return JsonResponse({'id': checkout_session.id})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def payment_success(request):
    """
    Sėkmingo mokėjimo puslapis
    Vartotojas nukreipiamas čia po sėkmingo Stripe checkout
    """
    session_id = request.GET.get('session_id')

    if not session_id:
        messages.error(request, 'No session ID provided')
        return redirect('dashboard')

    try:
        # Gauti Stripe session informaciją
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            # Pridėti kreditus į vartotojo sąskaitą
            metadata = session.metadata
            report_type = metadata.get('report_type')
            quantity = int(metadata.get('quantity'))

            # Sukurti ReportPackage
            from .models import ReportPackage
            package = ReportPackage.objects.create(
                user=request.user,
                package_type=str(quantity),
                report_type=report_type,
                reports_remaining=quantity,
                total_reports=quantity,
                is_active=True
            )

            messages.success(
                request,
                f'Payment successful! You now have {quantity} {report_type.upper()} report credits.'
            )
        else:
            messages.warning(request, 'Payment is still processing.')

    except Exception as e:
        messages.error(request, f'Error processing payment: {str(e)}')

    return redirect('dashboard')


@login_required
def payment_cancel(request):
    """
    Atšaukto mokėjimo puslapis
    """
    messages.info(request, 'Payment was cancelled.')
    return redirect('buy_credits')


@login_required
@require_http_methods(["POST"])
def stripe_webhook(request):
    """
    Stripe webhook endpoint
    Apdoroja Stripe event'us (payment_intent.succeeded, etc.)
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Apdoroti įvykį
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session_completed(session)

    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_succeeded(payment_intent)

    return JsonResponse({'status': 'success'})


def handle_checkout_session_completed(session):
    """Apdoroti užbaigtą checkout sesiją"""
    # Čia galima pridėti papildomą logiką
    pass


def handle_payment_succeeded(payment_intent):
    """Apdoroti sėkmingą mokėjimą"""
    # Čia galima pridėti papildomą logiką
    pass
