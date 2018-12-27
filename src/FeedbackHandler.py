import sys
from flask import Flask, request, jsonify, abort, send_from_directory, render_template
from ConfigImport import ConfigImport

# define the constants and variables
Config = ConfigImport()

class FeedbackHandler:
    def __init__(self, app):
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

                    ## TODO: log the feedback to a csv log file in structured way

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