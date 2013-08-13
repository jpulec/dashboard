from django.contrib import admin

from dashboard.apps.models import ServiceGroup, ServiceStatus, Environment

admin.site.register(ServiceGroup)
admin.site.register(ServiceStatus)
admin.site.register(Environment)
