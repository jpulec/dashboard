import datetime, logging
from django_rq import job
from suds.client import Client
from urlparse import urlparse
from rq.job import Job
import suds
import sure
import re
from dashboard.apps.gatherer.models import ServiceStatus, ServiceGroup, Environment
import dashboard.apps.webservices.tests.common as test_module
from dashboard.apps.gatherer.util import HTTPSClientCertTransport

logger = logging.getLogger(__name__)

@job
def call_webservice(test):
    #obj, created = ServiceStatus.objects.get_or_create(display_name=test["name"],
    #        defaults = {
    #            'dttm': datetime.datetime.now(),
    #            'status': 'ok',
    #            'status_description': "",
    #            'environment': Environment.objects.get_or_create(name="Test",
    #                service_group =ServiceGroup.objects.get_or_create(name="Web Services")[0])[0]
    #            }
    #        )
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
    #        return list()
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
    results = {}
    for op, validator in test['operations'].iteritems():
        results[op] = (validator, None)
        try:
            func = getattr(client.service[test['port']], op)
            results[op] = (validator, func())
        except (suds.MethodNotFound, suds.PortNotFound, suds.ServiceNotFound, suds.TypeNotFound, Exception) as e:
            print e
            continue
    return results

@job
def validate_webservice(test, job_id):
    job = Job.fetch(job_id)
    while not job.is_finished:
        continue
    obj = ServiceStatus.objects.get(display_name=test['name'])
    for operation, result in job.result.iteritems():
        validate = getattr(test_module, result[0][0])
        validate_args = getattr(test_module, result[0][1])
        try:
            if not validate(validate_args)(result[1]):
                if obj.status == "ok":
                    obj.status = "warn"
                logging.warning("Validation failed for %s - %s with value %s" % (test['name'], operation, str(result))) 
                #op_dict['status_description'] = settings_module.STATUSES[op_dict['status']]
                #op_dict['status_description'] += ("Validation failed for %s - %s" % (self.name, op)) 
                # if any item in the list fails validation, break
                # from loop leaving status as warn / error if error
                # was already set
                break
        except Exception as e:
            logging.error(e)
