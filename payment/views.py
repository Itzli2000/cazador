from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from annoying.decorators import render_to

from orders.models import OrderItem, Order
from orders.payment import send_mail
from cart.cart import Cart
from utilities.constants import SHIPPING_COST


@render_to('done.html')
@csrf_exempt
def payment_done(request):
    domain = settings.URL_DOMAIN
    invoice_number = request.session.get('invoice_str', None)
    message = ""
    user = request.user

    if not invoice_number:
        message = "Error en la creación de la orden."
        return {
            "message": message
        }

    # Check if the order exist
    try:
        order = Order.objects.get(user=user, reference_code=invoice_number)
        message = "La orden ya ha sido creada."
    except Order.DoesNotExist:
        cart = Cart(request)
        total = cart.get_total_price() + SHIPPING_COST
        order = Order()
        order.user = request.user
        order.reference_code = invoice_number
        order.transaction_id = order.id
        order.reference_pol = ''
        order.status = "PENDIENTE"
        order.method = "PAYPAL"
        order.save()

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        ctx = {
            'total': total,
            "reference": order.reference_code,
            "domain": domain,
        }

        send_mail(request, ctx, "card")

        # Clear the cart
        del request.session['invoice_str']
        cart.clear()

    return {
        "message": message
    }


@csrf_exempt
@render_to('canceled.html')
def payment_canceled(request):
    invoice_number = None
    message = ""
    user = request.user

    if not invoice_number:
        message = "Error en la creación de la orden."
        return {
            "message": message
        }

    # Check if the order exist
    try:
        order = Order.objects.get(user=user, reference_code=invoice_number)
        message = "La orden ya ha sido creada."
    except Order.DoesNotExist:
        cart = Cart(request)
        order = Order()
        order.user = request.user
        order.reference_code = invoice_number
        order.transaction_id = order.id
        order.reference_pol = ''
        order.status = "ERROR PAYPAL"
        order.method = "PAYPAL"
        order.save()

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

    return {
        "message": message,
        "invoice_number": invoice_number
    }
