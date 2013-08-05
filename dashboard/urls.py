from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dashboard.apps.gatherer.views import Home

urlpatterns = patterns('',
    # Examples:
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Home.as_view(), name="home"),
)
