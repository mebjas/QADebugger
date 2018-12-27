from flask import Flask, request, jsonify, abort, send_from_directory, render_template
from ConfigImport import ConfigImport

# define the constants and variables
Config = ConfigImport()

class BaseHanlders:
    def __init__(self, app):
        global Config

        app.config.update(
            TESTING=True,
            DEBUG=True,
            TEMPLATES_AUTO_RELOAD = True
        )     

        @app.route('/js/<path:path>')
        def send_js(path):
            print (path)
            return send_from_directory('js', path)

        @app.before_request
        def option_autoreply():
            """ Always reply 200 on OPTIONS request """
            if request.method == 'OPTIONS':
                resp = app.make_default_options_response()
                headers = None
                if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
                    headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

                h = resp.headers
                h['Access-Control-Allow-Origin'] = request.headers['Origin']
                h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
                h['Access-Control-Max-Age'] = "10"

                if headers is not None:
                    h['Access-Control-Allow-Headers'] = headers

                return resp

        @app.after_request
        def set_allow_origin(resp):
            """ Set origin for GET, POST, PUT, DELETE requests """

            h = resp.headers
            if request.method != 'OPTIONS' and 'Origin' in request.headers:
                h['Access-Control-Allow-Origin'] = request.headers['Origin']

            return resp

        # todo: remove this method
        @app.route('/')
        def hello_world():
            return 'Hello, World!'

        @app.route('/portal')
        def portal():
            return render_template('index.htm')
