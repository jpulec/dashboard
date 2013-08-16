from django.contrib import admin

from dashboard.apps.webservices.models import WebServiceTest, WebServiceCommand, WebServiceSSHCommand, WebServiceSSHTest, WebServiceSSHResult

admin.site.register(WebServiceTest)
admin.site.register(WebServiceCommand)
admin.site.register(WebServiceSSHCommand)
admin.site.register(WebServiceSSHTest)
admin.site.register(WebServiceSSHResult)
