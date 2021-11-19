import sys

from mysite.wsgi import application

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

PORT = int(sys.argv[1])

pywsgi.WSGIServer(
    ("0.0.0.0", PORT), application, handler_class=WebSocketHandler
).serve_forever()
