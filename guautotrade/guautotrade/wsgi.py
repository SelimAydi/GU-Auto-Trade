"""
WSGI config for guautotrade project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

# Production settings
sys.path.append('/var/www')
sys.path.append('/var/www/guautotrade_site/guautotrade')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guautotrade.settings")

application = get_wsgi_application()
