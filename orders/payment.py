from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

from cart.cart import Cart
from utilities.constants import SHIPPING_COST

import conekta

from accounts.models import Profile, ShippingAddress

conekta.api_key = settings.CONEKTA_API_KEY
conekta.api_version = "2.0.0"


def payment_oxxo(request):

    profile = Profile.objects.get(user=request.user)
    shipping_address = ShippingAddress.objects.get(user=request.user)

    items = []
    cart = Cart(request)
    for item in cart:
        cart_item = {}
        product = item['product']
        cart_item["name"] = product.name
        cart_item["description"] = product.description
        cart_item["unit_price"] = int(item["price"]) * 100
        cart_item["quantity"] = item["quantity"]
        items.append(cart_item)

    charge = conekta.Order.create({
        "line_items": items,
        "shipping_lines": [{
            "amount": SHIPPING_COST,
            "carrier": "El Gran Cazador México"
        }],
        'currency': "MXN",
        "customer_info": {
            "name": profile.name,
            "email": request.user.email,
            "phone": shipping_address.phone_number
        },
        "shipping_contact": {
            "phone": shipping_address.phone_number,
            "receiver":  profile.name,
            "address": {
                "street1": shipping_address.line1,
                "city": shipping_address.city,
                "state": shipping_address.state,
                "country": "MX",
                "postal_code": shipping_address.zip_code,
                "residential": "true"
            }
        },
        "charges": [{
            "payment_method": {
                "type": "oxxo_cash"
            }
        }]
    })

    return charge


def payment_card(request, token_id):

    profile = Profile.objects.get(user=request.user)
    shipping_address = ShippingAddress.objects.get(user=request.user)

    items = []
    cart = Cart(request)
    try:
        customer = conekta.Customer.create({
            'name': profile.name,
            'email': request.user.email,
            'phone': shipping_address.phone_number,
            'payment_sources': [{
                'type': 'card',
                'token_id': token_id
            }]
        })
    except conekta.ConektaError as e:
        print(e.message)

    for item in cart:
        # Create the list of articles to pass to conekta
        cart_item = {}
        product = item['product']
        cart_item["name"] = product.name
        cart_item["description"] = product.description
        cart_item["unit_price"] = int(item["price"]) * 100
        cart_item["quantity"] = item["quantity"]
        items.append(cart_item)

    try:
        conekta_order = conekta.Order.create({
            "line_items": items,
            "shipping_lines": [{
                "amount": SHIPPING_COST,
                "carrier": "El Gran Cazador México"
            }],
            "currency": "MXN",
            "card": token_id,
            "customer_info": {
                "customer_id": customer.id,
            },
            "shipping_contact": {
                "phone": shipping_address.phone_number,
                "receiver": profile.name,
                "address": {
                    "street1": shipping_address.line1,
                    "city": shipping_address.city,
                    "state": shipping_address.state,
                    "country": "MX",
                    "postal_code": shipping_address.zip_code,
                    "residential": True
                }
            },
            "charges": [{
                "payment_method": {
                    "payment_source_id": customer["payment_sources"][0]["id"],
                    "type": "card"
                    }
                }]
            })

        return conekta_order
    except conekta.ConektaError as e:
        return e.error_json['message']


def send_mail(request, ctx, payment_type):
    # Send mail to user
    subject = "Comprobante de pago"
    to = [request.user.email]
    from_email = "postmaster@egcm.mx"
    if payment_type == "oxxo":
        message = get_template("mail/oxxo_email.html").render(
                    Context(ctx)
        )
    else:
        message = get_template("mail/card_email.html").render(
                    Context(ctx)
        )
    msg = EmailMessage(
        subject, message, to=to, from_email=from_email
    )
    msg.content_subtype = "html"
    msg.send()
