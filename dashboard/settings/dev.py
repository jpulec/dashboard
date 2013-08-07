from common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATIC_ROOT = os.path.join(BASE_DIR, '/static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware','django_pdb.middleware.PdbMiddleware',)

INSTALLED_APPS += ('debug_toolbar','django_pdb')

TEMPLATE_CONTEXT_PROCESSORS += ( 'django.core.context_processors.debug',)

BROKER_URL = 'redis://localhost:6379/0'

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
