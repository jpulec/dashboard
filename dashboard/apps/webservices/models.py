from django.db import models
import logging
from suds.client import Client
from urlparse import urlparse
import suds
from dashboard.apps.gatherer.util import HTTPSClientCertTransport


logger = logging.getLogger(__name__)


class WebServiceTest(models.Model):
    ACCESS_CHOICES = (
            ("ESB", "ESB"),
            ("RPC", "RPC"),
        )
    SECURITY_CHOICES = (
            ("ssl", "SSL"),
            ("ws-security", "WS-Security"),
        )

    name = models.CharField(max_length=256)
    access = models.CharField(max_length=256, choices=ACCESS_CHOICES)
    url = models.URLField()
    security = models.CharField(max_length=12, choices=SECURITY_CHOICES)
    port = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name + " on port " + self.port

    def setup(self):
        client = None
        if self.security == "ssl":
            t = HTTPSClientCertTransport(
                    "ssl/test/dashboard_webservices_client_key.pem",
                    "ssl/test/dashboard_webservices_client_cert.pem")
            parsed = urlparse(self.url)
            location = parsed.scheme + "s://" + parsed.netloc + "/cert"
            try:
                client = Client(
                        self.url,
                        faults=False,
                        location=location,
                        transport=t)
            except Exception as e:
                logging.exception(e)
        return client

class WebServiceOperation(models.Model):
    name = models.CharField(max_length=256)
    validator = models.CharField(max_length=256)
    service = models.ForeignKey('WebServiceTest')

    def __unicode__(self):
        return self.name + " on service " + str(self.service)

    def execute(self):
        client = self.service.setup()
        result = None
        try:
            func = getattr(client.service[self.service.port], self.name)
            result = func()
        except (suds.MethodNotFound, suds.PortNotFound, suds.ServiceNotFound, suds.TypeNotFound, Exception) as e:
            logging.exception(e)
        return result
