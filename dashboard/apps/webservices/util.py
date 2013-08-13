import urllib2 as u2
import ssl
from suds.transport.http import HttpTransport, Reply, TransportError
from suds.plugin import DocumentPlugin
import xml.etree.ElementTree as ET
import httplib


class PIParser(ET.XMLTreeBuilder):

    def __init__(self):
        ET.XMLTreeBuilder.__init__(self)
        # assumes ElementTree 1.2.X
        self._parser.CommentHandler = self.handle_comment
        self._parser.ProcessingInstructionHandler = self.handle_pi
        self._target.start("document", {})

    def close(self):
        self._target.end("document")
        return ET.XMLTreeBuilder.close(self)

    def handle_comment(self, data):
        self._target.start(ET.Comment, {})
        self._target.data(data)
        self._target.end(ET.Comment)

    def handle_pi(self, target, data):
        self._target.start(ET.PI, {})
        self._target.data(target + " " + data)
        self._target.end(ET.PI)


def parse(source):
    return ET.parse(source, PIParser())


class HTTPSClientAuthHandler(u2.HTTPSHandler):

    def __init__(self, key, cert):
        u2.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        # Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)


class HTTPSClientCertTransport(HttpTransport):

    def __init__(self, key, cert, *args, **kwargs):
        HttpTransport.__init__(self, *args, **kwargs)
        self.key = key
        self.cert = cert

    def u2open(self, u2request):
        """
        Open a connection.
        @param u2request: A urllib2 request.
        @type u2request: urllib2.Requet.
        @return: The opened file-like urllib2 object.
        @rtype: fp
        """
        tm = self.options.timeout
        url = u2.build_opener(HTTPSClientAuthHandler(self.key, self.cert))
        return url.open(u2request, timeout=tm)


class MyPlugin(DocumentPlugin):
    # Stupid ass fixes for either malformed xml, or suds is picky/incorrect
    # with needing elements to correctly list their types

    def loaded(self, context):
        context.document = context.document.replace(
            "<xsd:element ref=\"APPT\" minOccurs=\"0\" />",
            "<xsd:complexType ref=\"APPT\" minOccurs=\"0\"/>")
        context.document = context.document.replace(
            "<xsd:element ref=\"APPOINTMENTS\" minOccurs=\"0\" maxOccurs=\"1\" />",
            "<xsd:complexType ref=\"APPOINTMENTS\" minOccurs=\"0\" maxOccurs=\"1\"/>")
