from django.conf.urls import url

import blog.views

urlpatterns = [
    url(r'^$', blog.views.home, name='blog_home'),
    url(r'^categoria/(?P<slug>[^\.]+)$',
        blog.views.view_category,
        name='view_category'),
    url(r'^(?P<slug>[^\.]+)/$',
        blog.views.view_post,
        name='view_post'
        ),
]
