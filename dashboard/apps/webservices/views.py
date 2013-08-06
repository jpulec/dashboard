from django.views.generic.base import View
from django.views.generic.list import MultipleObjectsMixin
from dashboard.apps.gatherer.models import ServiceStatus, ServiceGroup, Environment
from dashboard.apps.gatherer.tests.test import service_tests
from dashboard.apps.gatherer.util import HTTPSClientCertTransport
import datetime, logging
import suds
from suds.client import Client
from urlparse import urlparse

class WebServices(View, MultipleObjectsMixin):
    model = ServiceStatus
    allow_empty = True
    context_object_name = "webservices_list"

    def get_queryset():
        for test in service_tests:
            obj, created = ServiceStatus.objects.get_or_create(display_name=test["name"],
                    defaults = {
                        'dttm': datetime.datetime.now(),
                        'status': 'ok',
                        'status_description': "",
                        'service_group': ServiceGroup.objects.get_or_create(name="Web Services",
                                                                            environment = Environment.objects.get_or_create(name="Test")[0]
                            )[0]
                        }
                    )
            service_dicts = []
            client = None
            if test['security'] == "ssl":
                t = HTTPSClientCertTransport(
                    "ssl/test/dashboard_webservices_client_key.pem",
                    "ssl/test/dashboard_webservices_client_cert.pem")
                parsed = urlparse(test['url'])
                location = parsed.scheme + "s://" + parsed.netloc + "/cert"
                try:
                    client = Client(
                        test['url'],
                        faults=False,
                        location=location,
                        transport=t)
                except Exception as e:
                    logging.exception(e)
                    return list()
            #elif test['security'] == "ws-security":
            #    security = Security()
            #    token = UsernameToken(
            #        settings_module.ESB_USERNAME,
            #        settings_module.ESB_PASSWORD)
            #    security.tokens.append(token)
            #    try:
            #        client = Client(self.url, faults=False)
            #        client.set_options(wsse=security)
            #    except Exception as e:
            #        logging.exception(e)
            #        return list()
            #error_codes = self.get_error_codes(self.url)
            for op in test['operations'].iterkeys():
                result = None
                try:
                    func = getattr(client.service[test['port']], op)
                    result = func()
                except (suds.MethodNotFound, suds.PortNotFound, suds.ServiceNotFound, suds.TypeNotFound, Exception) as e:
                    print e
                    continue
            if result is not None:
                obj.status = self.get_status(result[0])
            else:
                obj.status = "ok"
            obj.save()
        return queryset

    def get_status(self, value):
        if value == 200:
            return "ok"
        elif value >= 300 and value < 400:
            # looks like something may be an issue, but not an error
            return "warn"
        else:
            return "error"
