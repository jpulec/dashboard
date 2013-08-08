#from settings.test import LOG_FILE
from common import *

#logging.basicConfig(
#    format='%(asctime)s %(message)s',
#    filename=LOG_FILE,
#    level=logging.INFO)

server_tests = [
    {
        "ip": ""
    }
]

service_tests = [
    {
        "access": "RPC",
        "name": "Application",
        "url": "http://rpctest.services.wisc.edu/Application.wsdl",
        "security": "ssl",
        "port": "ApplicationServicePort",
        "operations": {
            "ping": ("validate_regex", "ping_regex"),
        }
    }]
testers=[
    {
        "access": "RPC",
        "name": "AuthZ",
        "url": "http://rpctest.services.wisc.edu/AuthZ.wsdl",
        "security": "ssl",
        "port": "AuthZServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "Calendar",
        "url": "http://rpctest.services.wisc.edu/Calendar.wsdl",
        "security": "ssl",
        "port": "CalendarServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "CMS",
        "url": "http://rpctest.services.wisc.edu/CMS.wsdl",
        "security": "ssl",
        "port": "CMSServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "Groups",
        "url": "http://rpctest.services.wisc.edu/Groups.wsdl",
        "security": "ssl",
        "port": "GroupsServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "FPMAccount",
        "url": "http://rpctest.services.wisc.edu/FPMAccount.wsdl",
        "security": "ssl",
        "port": "FPMAccountServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "HDTools",
        "url": "http://rpctest.services.wisc.edu/HDTools.wsdl",
        "security": "ssl",
        "port": "HDToolsServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "IMS",
        "url": "http://rpctest.services.wisc.edu/IMS.wsdl",
        "security": "ssl",
        "port": "IMSServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "Kerberos",
        "url": "http://rpctest.services.wisc.edu/Kerberos.wsdl",
        "security": "ssl",
        "port": "KerberosServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "Mail",
        "url": "http://rpctest.services.wisc.edu/Mail.wsdl",
        "security": "ssl",
        "port": "MailServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "NetID",
        "url": "http://rpctest.services.wisc.edu/NetID.wsdl",
        "security": "ssl",
        "port": "NetIDServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "ServiceAccount",
        "url": "http://rpctest.services.wisc.edu/ServiceAccount.wsdl",
        "security": "ssl",
        "port": "ServiceAccountServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "Services",
        "url": "http://rpctest.services.wisc.edu/Services.wsdl",
        "security": "ssl",
        "port": "ServicesServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "Template",
        "url": "http://rpctest.services.wisc.edu/Template.wsdl",
        "security": "ssl",
        "port": "TemplateServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "Test",
        "url": "http://rpctest.services.wisc.edu/Test.wsdl",
        "security": "ssl",
        "port": "TestServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "UDS",
        "url": "http://rpctest.services.wisc.edu/UDS.wsdl",
        "security": "ssl",
        "port": "UDSServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "UDSAdmin",
        "url": "http://rpctest.services.wisc.edu/UDSAdmin.wsdl",
        "security": "ssl",
        "port": "UDSAdminServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "UDSPerson",
        "url": "http://rpctest.services.wisc.edu/UDSPerson.wsdl",
        "security": "ssl",
        "port": "UDSPersonServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "RPC",
        "name": "WebISO",
        "url": "http://rpctest.services.wisc.edu/WebISO.wsdl",
        "security": "ssl",
        "port": "WebISOServicePort",
        "operations": {
            "ping": "",
        }
    },
    {
        "access": "ESB",
        "name": "CHUB 1.1",
        "url":
        "http://esbtest.services.wisc.edu/CHUB/WebService/chub-ws-1.1/chub.wsdl",
        "security": "ws-security",
        "port": "chubSoap11",
        "operations": {
            "GetCurrentTerms": ""
        }
    },
    {
        "access": "ESB",
        "name": "CHUB 1.2",
        "url":
        "http://esbtest.services.wisc.edu/CHUB/WebService/chub-ws-1.2/chub.wsdl",
        "security": "ws-security",
        "port": "chubSoap11",
        "operations": {
            "GetCurrentTerms": ""
        }
    },
    {
        "access": "ESB",
        "name": "CHUB 1.3",
        "url":
        "http://esbtest.services.wisc.edu/CHUB/WebService/chub-ws-1.3/chub.wsdl",
        "security": "ws-security",
        "port": "chubSoap11",
        "operations": {
            "GetCurrentTerms": ""
        }
    },
    {
        "access": "ESB",
        "name": "CHUB 1.4",
        "url":
        "http://esbtest.services.wisc.edu/CHUB/WebService/chub-ws-1.4/chub.wsdl",
        "security": "ws-security",
        "port": "chubSoap11",
        "operations": {
            "GetCurrentTerms": ""
        }
    }
]

ssh_tests = [
    {
        "name": "L4 Blocks",
        "host": "perky.doit.wisc.edu",
        "cmds": [{
                 "cmd": "/sbin/iptables -n -L RH-Firewall-1-INPUT",
                 "test":
                 (negate(validate_lines("REJECT", "144.92.170.2")), "warn"),
                 "warn":
                 "Address 144.92.170.2 is blocked from the L4 on host perky.doit.wisc.edu",
                 "sudo": True
                 }],
    },
    {
        "name": "PersonHub Lock Check",
        "host": "ares.doit.wisc.edu",
        "cmds": [{
                 "cmd":
                 "[ -f /opt/PersonHubToCampusService/PersonHubToCampusServiceClient.lck ]",
                 "test": (lambda x: True if x.succeeded else False, "ok"),
                 "ok": "PersonHub lock file exists",
                 "sudo": False
                 },
                 {
                     "cmd":
                     "'expr `date +\"%s\"` - `stat -c%Z /opt/PersonHubToCampusService/PersonHubToCampusServiceClient.lck`",
                     # Check if the file is less than an hour old
                     "test":
                     (lambda secs: False if secs.succeeded and int(secs)
                      >= 3600 else True, "warn"),
                     "warn": "PersonHub lock file is more than 1 hour old",
                     "sudo": False
                 }
                 ],
    }
]
