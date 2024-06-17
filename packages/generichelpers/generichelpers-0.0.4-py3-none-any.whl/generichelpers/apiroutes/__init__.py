"""Flask API app creator module"""

from __future__ import absolute_import
import sys
import os
from flask import Flask
# +++++++++++++++++
BASE_PATH = os.path.abspath("./generic-helpres/src")
extendPaths = [p for p in (os.path.dirname(BASE_PATH), BASE_PATH) if p not in sys.path]
sys.path = extendPaths + sys.path
# +++++++++++++++++


def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False

    from . import helperapis
    app.register_blueprint(helperapis.bp)

    @app.route('/isalive')
    def isalive():
        return ('<b style="color:blue;">Alive</b> - Helper APIs')
    return app
