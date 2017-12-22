from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^done/$', views.payment_done, name='done'),
    url(r'^canceled/$', views.payment_canceled, name='canceled'),
]
