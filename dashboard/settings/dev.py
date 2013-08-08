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

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    'high': {
        'URL': 'redis://localhost:6379',
        'DB': 0,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}
        
