from django.shortcuts import get_object_or_404
from annoying.decorators import render_to

from .models import Category, Menu
from blog.models import Post
from shop.models import Product


@render_to("main_menu.html")
def main_menu(request):
    categories = Category.objects.filter(is_active=True).order_by('order')
    return {
        'categories': categories
    }


@render_to("menu_category.html")
def menu_category(request, category_id):
    categories = Category.objects.filter(is_active=True).order_by('order')
    category = Category.objects.get(pk=category_id)
    products = Menu.objects.filter(is_active=True, category=category).order_by(
        'name'
    )
    related_products = Product.objects.filter(
        is_active=True,
    )[:3]
    menues = Menu.objects.filter(
        is_active=True,
        category=category
    )[:3]
    posts = Post.objects.all()[:3]
    return {
        'categories': categories,
        'category': category,
        'products': products,
        'menues': menues,
        'actual_category': int(category_id),
        'posts': posts,
        'related_products': related_products,
    }


@render_to("detail_menu.html")
def detail_menu(request, category_id, product_id):
    categories = Category.objects.filter(is_active=True).order_by('order')
    category = Category.objects.get(pk=category_id)
    products = Menu.objects.filter(is_active=True, category=category).order_by(
        'name'
    )
    product = get_object_or_404(Menu, pk=product_id, category=category)
    related_products = Product.objects.filter(
        is_active=True,
    )[:3]
    menues = Menu.objects.filter(
        is_active=True,
        category=category
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
