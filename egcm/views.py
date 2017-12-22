from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from annoying.decorators import render_to

from shop.models import Product
from blog.models import Post
from menues.models import Menu


@render_to('home.html')
def home(request):
    products = Product.objects.filter(is_available=True)[:6]
    menues = Menu.objects.filter(is_active=True)[:3]
    posts = Post.objects.all()[:3]

    return {
        'products': products,
        'menues': menues,
        'posts': posts
    }


@render_to('login.html')
def login_view(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/')
    return {}


def logout_view(request):
    logout(request)
    return redirect('/')
