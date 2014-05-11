from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'fphoto.views.home', name='home'),
    url(r'^dash$', 'fphoto.views.dash', name='dash'),
    url(r'^logout$', 'fphoto.views.logout', name='logout', ),

    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
