import sys
from flask import Flask, request, jsonify, abort, send_from_directory, render_template
from ConfigImport import ConfigImport
from Feedback import FeedbackLogger, FeedbackWriter

# define the constants and variables
Config = ConfigImport()
feedbackLogger = FeedbackLogger(Config.Get("logging/feedback/path"))
feedbackWriter = FeedbackWriter(feedbackLogger)

class FeedbackHandler:
    def __init__(self, app):
        @app.route('/api/v1/feedback/<feedbackFor>', methods=['POST'])
        def feedback(feedbackFor):
            try:
                if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
                    for key in ['correlationId', 'value', 'question', 'partAnswer']:
                        if key not in request.json:
                            raise "Invalid content, %s not present" % key

                    feedback = {
                        "Question": request.json["question"],
                        "PartAnswer": request.json["partAnswer"],
                        "CorrelationId": request.json["correlationId"],
                        "Value": request.json["value"]
                    }

                    feedbackWriter.Log(feedbackFor, feedback)
                    feedback["feedbackFor"] = feedbackFor

                    response = {}
                    response["apiversion"] = Config.Get("api/version")
                    response["result"] = {
                        "context": feedback
                    }

                    resp = jsonify(response)
                    resp.status_code = 200
                    return resp
            except:
                print (sys.exc_info())
                resp = jsonify({
                    'message': 'Internal Server Error, most likely an invalid input format.'})
                resp.status_code = 500
                return resp

            resp = jsonify({'message': 'Invalid Content-Type; Only application/json supported;'})
            resp.status_code = 400
            return resp