from django.shortcuts import get_object_or_404

from annoying.decorators import render_to

from .models import Category, Product
from blog.models import Post
from menues.models import Menu
from cart.forms import CartAddProductForm


@render_to("main_shop.html")
def shop(request):
    categories = Category.objects.filter(is_active=True).order_by('order')
    return {
        'categories': categories,
    }


@render_to("detail_product.html")
def detail_product(request, category_id):
    categories = Category.objects.filter(is_active=True).order_by('order')
    category = Category.objects.get(pk=category_id)
    cart_product_form = CartAddProductForm()
    products = Product.objects.filter(
        is_active=True,
        is_available=True,
        category=category).order_by('name')
    related_products = Product.objects.filter(
        is_active=True,
        category=category
    )[:3]
    menues = Menu.objects.filter(is_active=True)[:3]
    posts = Post.objects.all()[:3]
    return {
        'categories': categories,
        'category': category,
        'products': products,
        'related_products': related_products,
        'cart_product_form': cart_product_form,
        'menues': menues,
        'posts': posts,
        'actual_category': int(category_id),
    }


@render_to('detail_product_one.html')
def detail_product_one(requesst, category_id, product_id):
    categories = Category.objects.filter(is_active=True).order_by('order')
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(
        is_active=True,
        category=category
    ).order_by('name')
    product = get_object_or_404(Product, pk=product_id, category=category)
    related_products = Product.objects.filter(
        is_active=True,
        category=category
    )[:3]
    menues = Menu.objects.filter(
        is_active=True
    )[:3]
    posts = Post.objects.all()[:3]
    return {
        'categories': categories,
        'category': category,
        'product': product,
        'products': products,
        'menues': menues,
        'actual_category': int(category_id),
        'posts': posts,
        'related_products': related_products,
    }


@render_to("price_list.html")
def price_list(request):
    categories = Category.objects.filter(is_active=True).order_by('order')
    products = Product.objects.filter(
        is_active=True,
        is_available=True
    ).order_by('name')
    return {
        'categories': categories,
        'products': products,
    }
