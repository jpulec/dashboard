from django.db import models
import logging
from suds.client import Client
from urlparse import urlparse
import suds
from dashboard.apps.webservices.util import HTTPSClientCertTransport
from dashboard.apps.models import SSHTest, SSHPipe, SSHCommand, ServiceCommand, ServiceTest
from dashboard.apps.webservices.tests import common as test_module
import os,sys
import json
import time


logger = logging.getLogger(__name__)


class WebServiceTest(ServiceTest):
    ACCESS_CHOICES = (
            ("ESB", "ESB"),
            ("RPC", "RPC"),
        )
    SECURITY_CHOICES = (
            ("ssl", "SSL"),
            ("ws-security", "WS-Security"),
        )

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
                        faults=True,
                        location=location,
                        transport=t)
            except Exception as e:
                logging.exception(e)
        return client

class WebServiceCommand(ServiceCommand):
    service = models.ForeignKey('WebServiceTest')
    validate_args_str = models.CharField(max_length=256)

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
        return self.validate(result)

    def validate(self, result):
        validate_func = None
        validate_args = None
        try:
            validate_func = getattr(test_module, self.validate_func_str)
            validate_args = getattr(test_module, self.validate_args_str)
        except AttributeError as e:
            logging.error(e)
            return ("error", self.failed_validation)
        try:
            if not validate_func(validate_args)(result):
                logging.warning("Validation failed for %s - %s with value %s" % (self.name, self.validate_func_str, str(result))) 
                return ("error", self.failed_validation)
        except Exception as e:
            logging.error(e)
            return ("error", self.failed_validation)
        return ("ok", "Service is operation normally.")

class WebServiceSSHTest(SSHTest):
    pass

class WebServiceSSHCommand(SSHCommand):
    test = models.ForeignKey('WebServiceSSHTest')

    def validate(self, result):
        validate_func = None
        try:
            validate_func = getattr(test_module, self.validate_func_str)
        except AttributeError as e:
            logging.error(e)
            return SSHPipe(result, True)
        try:
            if not validate_func(result):
                logging.warning("Validation failed for %s - %s with value %s" % (self.test.name, self.validate_func_str, result))
                return SSHPipe(result, True)
        except Exception as e:
            logging.error(e)
            return SSHPipe(result, True)
        return SSHPipe(result, False)
