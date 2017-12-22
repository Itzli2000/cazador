from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^pdf/$', views.oxxo_pdf, name='oxxo_pdf'),
    url(r'^hooks/$', views.process_webhook, name='hooks'),
]
