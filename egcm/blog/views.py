from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from annoying.decorators import render_to

from .models import Category, Post
from shop.models import Product
from menues.models import Menu


@render_to('blog_home.html')
def home(request):
    categories = Category.objects.filter(is_active=True)
    posts_list = Post.objects.filter(is_active=True)

    paginator = Paginator(posts_list, 5)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out or range, deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return {
        'categories': categories,
        'posts': posts,
    }


@render_to('post.html')
def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(
        category=post.category,
        is_active=True
    )[:3]

    related_products = Product.objects.filter(
        is_active=True,
    )[:3]

    products = Product.objects.filter(is_available=True)[:6]
    menues = Menu.objects.filter(is_active=True)[:3]

    return {
        'post': post,
        'related_posts': related_posts,
        'related_products': related_products,
        'products': products,
        'menues': menues,
    }


@render_to('category.html')
def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts_list = Post.objects.filter(is_active=True, category=category)

    paginator = Paginator(posts_list, 5)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out or range, deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return {
        'category': category,
        'posts': posts
    }
