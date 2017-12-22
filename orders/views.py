import json
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage

from annoying.decorators import render_to
from paypal.standard.forms import PayPalPaymentsForm

from .models import OrderItem, Order
from .payment import payment_oxxo, send_mail
from accounts.models import ShippingAddress, BillingAddress
from cart.cart import Cart
from utilities.utils import (
    get_or_create,
    render_to_pdf,
    generate_random_invoice_number
)
from utilities.constants import SHIPPING_COST


@login_required
@render_to('orders/create.html')
def order_create(request):
    cart = Cart(request)
    total = cart.get_total_price() + SHIPPING_COST
    shipping_address = get_or_create(ShippingAddress, request.user)
    billing_address = get_or_create(BillingAddress, request.user)
    host = request.get_host()
    invoice_str = generate_random_invoice_number()
    request.session['invoice_str'] = invoice_str
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % total.quantize(Decimal('.01')),
        'item_name': 'El Gran Cazador México, carrito de compras',
        'invoice': invoice_str,
        'currency_code': 'MXN',
        'custom': invoice_str,
        'notify_url': 'http://{}{}'.format(
            host,
            reverse('paypal-ipn')
        ),
        'return_url': 'http://{}{}'.format(
            host,
            reverse('payment:done')
        ),
        'cancel_return': 'http://{}{}'.format(
            host,
            reverse('payment:canceled')
        )
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    if request.method == 'POST':
        domain = settings.URL_DOMAIN

        order = Order()
        order.user = request.user
        order.reference_code = ''
        order.transaction_id = ''
        order.reference_pol = ''
        order.save()
        
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            ) 
        payment_type = request.POST.get('payment_type', '')
        
        # if the payment was made with oxxo
        if payment_type == 'oxxo':
            charge = payment_oxxo(request)

            order.method = "Oxxo"

            # Create the order with pending status
            order.status = 'PENDIENTE'
            order.reference_code = charge.charges[0]["payment_method"]["reference"]
            order.transaction_id = charge.id
            order.save()

            ctx = {
                "total": total,
                "reference": order.reference_code,
                "domain": domain,
            }

            send_mail(request, ctx, payment_type)

            # Clear the cart
            cart.clear()

            # Redirect to response with parameters
            return render(
                request,
                'orders/created.html',
                {
                    'order': order,
                }
            )

        return render(
            request,
            'orders/created.html',
            {
                'order': order,
            }
        )
    else:
        return {
            'cart': cart,
            'shipping_price': SHIPPING_COST,
            'total': total,
            'shipping_address': shipping_address,
            'billing_address': billing_address,
            'form': form
        }


@login_required
@render_to('orders/orders.html')
def view_order(request):
    orders = Order.objects.filter(user=request.user)
    items = OrderItem.objects.filter(order__in=orders)
    return {
        'orders': orders,
        'items': items
    }


@csrf_exempt
def process_webhook(request):
    event_json = json.loads(request.body)
    data = event_json['data']['object']

    if data['status'] == 'paid':
        order_id = data['order_id']

        order = get_object_or_404(Order, transaction_id=order_id)
        order.status = "PAGADO"
        order.paid = True
        order.save()

        # Send email to the user
        subject = "Su pago ha sido procesado"
        to = [order.user.email]
        from_email = "postmaster@egcm.mx"

        ctx = {
            'order': order,
        }

        message = get_template(
            'mail/user_order_email.html'
        ).render(Context(ctx))
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

        # Send mail to egcm to alert from paid oxxo
        subject = "Se ha procesado un pago"
        to = ["laura@yaxha.mx"]
        from_email = "postmaster@egcm.mx"

        ctx = {
            'order': order,
        }

        message = get_template(
            'mail/egcm_order_email.html'
        ).render(Context(ctx))
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

    return HttpResponse()


def oxxo_pdf(request):

    total = request.GET.get('total', '')
    reference = request.GET.get('reference', '')

    html_context = {
        "total": total,
        "reference": reference,
    }
    pdf = render_to_pdf('pdf/oxxo_pdf.html', html_context)
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="oxxo_pay.pdf"'
    return response
