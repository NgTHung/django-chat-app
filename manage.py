#!/usr/bin/env python3.9
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if (sys.argv[1] == "runserver"):
    from mysite.wsgi import application
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    ip,port = sys.argv[2].split(':')
    PORT = int(port)
    pywsgi.WSGIServer(
        ("0.0.0.0", PORT), application, handler_class=WebSocketHandler
    ).serve_forever()
else: main()
