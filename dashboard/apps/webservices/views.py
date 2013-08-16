from django.views.generic.base import View, TemplateView
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from dashboard.apps.models import ServiceStatus, ServiceGroup, Environment
from dashboard.apps.webservices.models import WebServiceTest, WebServiceCommand, WebServiceSSHCommand, WebServiceSSHTest
import datetime, logging
import django_rq

logger = logging.getLogger(__name__)

class WebServices(MultipleObjectMixin, TemplateView):
    model = ServiceStatus
    allow_empty = True
    template_name = "service_snippet.html"

    def get(self, request , *args, **kwargs):
        return super(WebServices, self).get(request, *args, object_list=self.get_queryset(), **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WebServices, self).get_context_data(**kwargs)
        context['service'] = ServiceGroup.objects.get(name="Web Services")
        context['envs'] = Environment.objects.filter(service_group=context['service'])
        return context

    def get_queryset(self):
        q = django_rq.get_queue("webservices")
        service_tests = WebServiceTest.objects.all()
        for service_test in service_tests:
            commands = WebServiceCommand.objects.filter(service=service_test)
            for command in commands:
                q.enqueue(command.execute)
        ssh_tests = WebServiceSSHTest.objects.all()
        for ssh_test in ssh_tests:
            commands = [command for command in sorted(WebServiceSSHCommand.objects.filter(test=ssh_test), cmp=lambda x,y: cmp(x.execution_number, y.execution_number))]
            q.enqueue(sync_ssh, commands)
        while not q.is_empty():
            continue
        queryset = list()
        group = ServiceGroup.objects.filter(name="Web Services")
        for env in Environment.objects.filter(service_group=group):
            env.last_updated = datetime.datetime.now()
            env.save()
            for status in ServiceStatus.objects.filter(environment=env):
                queryset.append(status)
        return queryset

def sync_ssh(commands):
    next_num = 1
    for command in commands:
        if command.execution_number != next_num:
            continue
        next_num = command.execute()
