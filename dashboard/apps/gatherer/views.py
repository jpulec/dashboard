# Create your views here.
from django.views.generic.list import ListView
from dashboard.apps.gatherer.models import ServiceStatus, ServiceGroup, Environment
from dashboard.apps.gatherer.tests.test import service_tests
from dashboard.apps.gatherer.util import HTTPSClientCertTransport
import datetime, logging
import suds
from suds.client import Client
from urlparse import urlparse

SERVICE_TEMPLATES = ["webservices_shim.html"]

class Home(ListView):

    template_name = "base.html"
    model = ServiceStatus

    def post(self, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['service_templates'] = SERVICE_TEMPLATES

    def get_queryset(self):
        queryset = dict()
        for group in ServiceGroup.objects.all():
            queryset[group.name] = dict()
            for env in Environment.objects.filter(service_group=group):
                queryset[group.name][env.name] = list()
                for status in ServiceStatus.objects.filter(environment=env):
                    queryset[group.name][env.name].append(status)
        return queryset
