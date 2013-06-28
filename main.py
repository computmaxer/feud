import sys, os

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
LIB_PATH = os.path.join(ROOT_PATH, 'lib')
sys.path.insert(0, LIB_PATH)

from flask import Flask

from flask_mongoengine import MongoEngine

import auth
from auth import urls as auth_urls

from base import urls as base_urls
from base.templatetags import ttags

from feud import urls as feud_urls

# Determining the project root.
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, static_folder=os.path.join(PROJECT_ROOT, 'static'), static_url_path='/static')

auth.initialize(app)

app.config['MONGODB_DB'] = 'wfeud'
app.config['SECRET_KEY'] = 'my_super_secret_key'

# Setting up the connection to the MongoDB backend.
db = MongoEngine(app)

#Define URLs
base_urls.setup_urls(app)
auth_urls.setup_urls(app)
feud_urls.setup_urls(app)

#Setup other things
ttags.setup_jinja2_environment(app)


from socketio import socketio_manage
from flask import request
from feud import views as feud_views


# Wanted a better place for this.  Couldn't get app to import elsewhere.  Oh well
@app.route("/socket.io/<path:path>")
def run_socketio(path):
    socketio_manage(request.environ, {'': feud_views.BuzzNamespace})
    return ''


# Copied this from https://github.com/kcarnold/flask-gevent-socketio-chat/
if __name__ == '__main__':
    print 'Listening on http://localhost:5000'
    app.debug = True
    import os
    from werkzeug.wsgi import SharedDataMiddleware
    app = SharedDataMiddleware(app, {
        '/': os.path.join(os.path.dirname(__file__), 'static')
        })
    from socketio.server import SocketIOServer
    SocketIOServer(
        ('0.0.0.0', 5000),
        app, namespace="socket.io",
        policy_server=False).serve_forever()
