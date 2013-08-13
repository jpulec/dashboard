from django.contrib import admin

from dashboard.apps.webservices.models import WebServiceTest, WebServiceOperation

admin.site.register(WebServiceTest)
admin.site.register(WebServiceOperation)
