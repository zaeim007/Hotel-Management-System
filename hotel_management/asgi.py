"""
ASGI config for hotel_management project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')

application = get_asgi_application()
