import os
import sys
import pandas as pd
import abc

class FeedbackLogger:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)

    def Push(self, filename, df):
        print ("FeedbackLogger.Push")

        fullpath = "%s/%s" % (self.path, filename)
        if os.path.isfile(fullpath):
            with open(fullpath, 'a') as ofp:
                df.to_csv(ofp, header=False, index=False)

        else:
            with open(fullpath, 'w') as ofp:
                df.to_csv(ofp, index=False)


class FeedbackWriter:
    def __init__(self, logger):
        self.logger = logger

    def Log(self, feedbackFor, feedback):
        df = pd.DataFrame(feedback, index=[0])
        self.logger.Push("%s.csv" % feedbackFor, df)