from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views as flatpages_views

from . import views as egcm_views
from shop import views as shop_views
from menues import views as menu_views
from accounts import views as accounts_views
from orders import views as order_views


urlpatterns = [

    url(r'^$', egcm_views.home, name='home'),
    url(
        r'^nosotros/$', flatpages_views.flatpage,
        {'url': '/nosotros/'},
        name='about'
    ),

    url(r'^carnes-exoticas/$', shop_views.shop, name='shop'),
    url(
        r'^carnes-exoticas/(?P<category_id>[0-9]+)/$',
        shop_views.detail_product,
        name='detail_product'
    ),
    url(
        r'^carnes-exoticas/(?P<category_id>[0-9]+)/(?P<product_id>[0-9]+)$',
        shop_views.detail_product_one,
        name='detail_product_one'
    ),

    url(r'^iniciar_sesion/$', egcm_views.login_view, name="login"),
    url(r'^cerrar_sesion/$', egcm_views.logout_view, name="logout"),
    url(r'^registro/$', accounts_views.register, name="register"),
    url(
        r'^cambiar-contrasena/$',
        accounts_views.change_password,
        name="change_pass"
    ),
    url(
        r'^envio/$',
        accounts_views.shipping,
        name="shipping"
    ),
    url(
        r'^facturacion/$',
        accounts_views.billing,
        name="billing"
    ),
    url(
        r'^pedidos/$',
        order_views.view_order,
        name='orders'
    ),
    url(r'^activacion/(?P<key>.+)$', accounts_views.activation,
        name="activation"),
    url(r'^nueva_activacion$', accounts_views.new_activation_link,
        name="new_activation_link"),
    url(r'^perfil/$', accounts_views.profile, name="profile"),

    url(r'^menu/$', menu_views.main_menu, name='menu'),
    url(
        r'^menu/(?P<category_id>[0-9]+)/$',
        menu_views.menu_category,
        name='menu_category'
    ),
    url(
        r'^menu/(?P<category_id>[0-9]+)/(?P<product_id>[0-9]+)$',
        menu_views.detail_menu,
        name='detail_menu'
    ),

    url(r'lista-de-precios/', shop_views.price_list, name="price_list"),

    url(r'^blog/', include('blog.urls')),
    url(r'^contacto/', include('contact.urls')),
    url(r'^accounts/', include('accounts.urls')),

    url(r'^carrito/', include('cart.urls', namespace='cart')),
    url(r'^ordenes/', include('orders.urls', namespace='orders')),

    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^payment/', include('payment.urls', namespace='payment')),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
