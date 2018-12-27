import sys
import json
from flask import Flask, request, jsonify, abort, send_from_directory, render_template
from functools import wraps
from ConfigImport import ConfigImport
from Model import Model

# define the constants and variables
Config = ConfigImport()

class QuestionHandler:
    def __init__(self, app):
        model = Model()

        @app.route('/api/v1/question', methods=['POST'])
        def question():
            global Config
            try:
                if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
                    if "question" not in request.json:
                        raise "Invalid content, question not present"
                    
                    response = {}
                    response["apiversion"] = Config.Get("api/version")
                    response["result"] = model.Answer(request.json["question"])

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