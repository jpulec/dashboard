from django.contrib import admin

from dashboard.apps.webservices.models import WebServiceTest, WebServiceCommand, WebServiceSSHCommand, WebServiceSSHTest

admin.site.register(WebServiceTest)
admin.site.register(WebServiceCommand)
admin.site.register(WebServiceSSHCommand)
admin.site.register(WebServiceSSHTest)
