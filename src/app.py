import sys
import json
from flask import Flask
from functools import wraps
from ConfigImport import ConfigImport
from BaseHanlders import BaseHanlders
from QuestionHandler import QuestionHandler
from FeedbackHandler import FeedbackHandler

# define the constants and variables
Config = ConfigImport()
app = Flask(__name__, static_url_path='/static')
BaseHanlders(app)
QuestionHandler(app)
FeedbackHandler(app)

if __name__ == '__main__':
    app.run(host=Config.Get("server/host"), port=Config.Get("server/port"))
    print ("Shutting down...")

