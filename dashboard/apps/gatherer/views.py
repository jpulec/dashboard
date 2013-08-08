# Create your views here.
from django.views.generic.base import TemplateView
import logging

SERVICE_TEMPLATES = ["webservice_shim.html"]

logger = logging.getLogger(__name__)

class Home(TemplateView):

    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['service_templates'] = SERVICE_TEMPLATES
        return context
