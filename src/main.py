import sys
import json
from flask import Flask, request, jsonify, abort, send_from_directory, render_template
from functools import wraps
from ConfigImport import ConfigImport
from QuestionHandler import QuestionHandler

# define the constants and variables
Config = ConfigImport()
questionHandler = QuestionHandler()

app = Flask(__name__, static_url_path='/static')
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

@app.route('/api/v1/question', methods=['POST'])
def question():
    global Config
    global questionHandler
    try:
        if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
            if "question" not in request.json:
                raise "Invalid content, question not present"
            
            response = {}
            response["apiversion"] = Config.Get("api/version")
            response["result"] = questionHandler.Answer(request.json["question"])

            resp = jsonify(response)
            resp.status_code = 200
            return resp
    except:
        print (sys.exc_info()[1])
        resp = jsonify({
            'message': 'Internal Server Error, most likely an invalid input format.',
            'exception': sys.exc_info()})
        resp.status_code = 500
        return resp

    resp = jsonify({'message': 'Invalid Content-Type; Only application/json supported;'})
    resp.status_code = 400
    return resp

@app.route('/api/v1/feedback/<feedbackFor>', methods=['POST'])
def feedback(feedbackFor):
    try:
        if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
            for key in ['correlationId', 'value', 'question', 'partAnswer']:
                if key not in request.json:
                    raise "Invalid content, %s not present" % key
            
            response = {}
            response["apiversion"] = Config.Get("api/version")
            response["result"] = {
                "context": {
                    "feedbackFor": feedbackFor,
                    "correlationId": request.json["correlationId"],
                    "value": request.json["value"],
                    "question": request.json["question"],
                    "partAnswer": request.json["partAnswer"]
                }
            }

            resp = jsonify(response)
            resp.status_code = 200
            return resp
    except:
        print (sys.exc_info()[1])
        resp = jsonify({
            'message': 'Internal Server Error, most likely an invalid input format.',
            'exception': sys.exc_info()})
        resp.status_code = 500
        return resp

    resp = jsonify({'message': 'Invalid Content-Type; Only application/json supported;'})
    resp.status_code = 400
    return resp

if __name__ == '__main__':
    app.run(host=Config.Get("server/host"), port=Config.Get("server/port"))
    print ("Shutting down...")

