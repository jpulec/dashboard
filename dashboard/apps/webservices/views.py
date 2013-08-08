from django.views.generic.base import View, TemplateView
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from django.http import HttpResponse
from dashboard.apps.gatherer.models import ServiceStatus, ServiceGroup, Environment
from dashboard.apps.webservices.tests.test import service_tests
from dashboard.apps.webservices.tests.common import validate_regex
from dashboard.apps.gatherer.util import HTTPSClientCertTransport
from django.shortcuts import render_to_response
from django.template import RequestContext
from dashboard.apps.webservices.tasks import call_webservice
import datetime, logging
import suds
import django_rq
import threading
from suds.client import Client
from urlparse import urlparse

logger = logging.getLogger(__name__)

class WebServices(MultipleObjectMixin, TemplateView):
    model = ServiceStatus
    allow_empty = True
    template_name = "webservice_shim.html"
    context_object_name = "webservices_list"

    def get(self, request , *args, **kwargs):
        return super(WebServices, self).get(request, *args, object_list=self.get_queryset(), **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WebServices, self).get_context_data(**kwargs)
        context['service'] = ServiceGroup.objects.get(name="Web Services")
        context['envs'] = Environment.objects.filter(service_group=context['service'])
        return context

    def get_queryset(self):
        jobs = []
        for test in service_tests:
            jobs.append(call_webservice.delay(test))
        while not django_rq.get_queue().is_empty():
            #Twiddle your fucking thumbs
            pass
        for job in jobs:
            self.validate(job)
        queryset = list()
        group = ServiceGroup.objects.filter(name="Web Services")
        for env in Environment.objects.filter(service_group=group):
            env.last_updated = datetime.datetime.now()
            env.save()
            for status in ServiceStatus.objects.filter(environment=env):
                queryset.append(status)
        return queryset
    
    def validate(self, job_result):
        

    def get_status(self, value):
        if value == 200:
            return "ok"
        elif value >= 300 and value < 400:
            # looks like something may be an issue, but not an error
            return "warn"
        else:
            return "error"
