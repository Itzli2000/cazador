from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from annoying.decorators import render_to

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from utilities.constants import SHIPPING_COST
from blog.models import Post
from menues.models import Menu


@require_POST
def cart_add(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id', "")
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )

        return HttpResponse(status=201)

    return HttpResponse(status=400)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


@render_to('cart_detail.html')
def cart_detail(request):
    menues = Menu.objects.filter(is_active=True)[:3]
    posts = Post.objects.all()[:3]
    related_products = Product.objects.filter(
        is_active=True,
    )[:3]
    cart = Cart(request)
    total = cart.get_total_price() + SHIPPING_COST
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True,
                'shipping_price': SHIPPING_COST,
                'total': total,
                'menues': menues,
                'posts': posts,
                'related_products': related_products,
            }
        )
    return {
        'cart': cart,
        'shipping_price': SHIPPING_COST,
        'total': total,
        'menues': menues,
        'posts': posts,
        'related_products': related_products,
    }
