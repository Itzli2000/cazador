from django.conf.urls import url
import django.contrib.auth.views as django_views

import accounts.views

urlpatterns = [
    url(r'^password/reset/$', accounts.views.password_reset,
        name='password_reset'),
    url(r'^password/reset/done/$', accounts.views.password_reset_done,
        name='password_reset_done'),
    url(r'^password/change/$', accounts.views.change_password,
        name='password_change'),
    url(r'^password/change/done$', accounts.views.password_change_done,
        name='password_change_done'),
    url(r'^password/reset/done/$',
        accounts.views.password_reset_done),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        django_views.password_reset_confirm,
        {'post_reset_redirect': '/accounts/password/done/',
        'template_name': 'custom_registration/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^password/done/$',
        accounts.views.password_change_done),
]

