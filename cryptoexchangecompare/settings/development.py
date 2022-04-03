from .base import *

DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.ce.sharif.edu'
EMAIL_HOST_USER = 'alihosseini@ce.sharif.edu'
EMAIL_HOST_PASSWORD = 'qweasdzxc1'
EMAIL_PORT = '587'

DOMAIN = '127.0.0.1:8000'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
#         },
#     },
# }
