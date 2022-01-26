"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os,sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# activate_this = "C:/Users/BBQPa/Documents/mysite/mychatapp/Scripts/activate_this.py"
# with open(activate_this) as f:
#     exec(f.read(), {'__file__': activate_this})
# os.environ['PYTHONPATH'] = 'C:/Users/BBQPa/Documents/mysite/mychatapp/lib/site-packages'

from django.core.wsgi import get_wsgi_application

django_app = get_wsgi_application()

import socketio

from login.views import sio

application = socketio.WSGIApp(sio, django_app)

