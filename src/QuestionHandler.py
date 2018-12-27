import uuid

class QuestionHandler:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def Answer(self, question):
        if question.strip() == "":
            raise "InvalidQuestionException"

        correlationId = uuid.uuid4()
        response = {}
        response["question"] = question
        response["uuid"] = correlationId

        ## TODO: this is temporary
        response["answer"] = "there is a lever to the right of driver seat, use that to adjust"

        ## Widget constuction
        response["widgets"] = []

        answerFeedbackWidget = {
            "key": "Over Feedback",
            "value": None,
            "displayContract": "text",
            "widgetType": "small",
            "feedbackUrl": "/api/v1/feedback/answer"
        }

        answerTypeDetectionWidget = {
            "key": "Answer Type",
            "value": "paragraph",
            "displayContract": "text",
            "widgetType": "small",
            "feedbackUrl": "/api/v1/feedback/answerTypeDetection"
        }

        keywordsWidget = {
            "key": "Formed Queries (keywords)",
            "value": "adjust, driver, seat",
            "displayContract": "text",
            "widgetType": "small",
            "feedbackUrl": "/api/v1/feedback/keywords"
        }

        questionTypeWidget = {
            "key": "Question Type classification",
            "value": "How",
            "displayContract": "text",
            "widgetType": "small",
            "feedbackUrl": "/api/v1/feedback/questionTypeDetection"
        }

        response["widgets"].append(answerFeedbackWidget)
        response["widgets"].append(answerTypeDetectionWidget)
        response["widgets"].append(keywordsWidget)
        response["widgets"].append(questionTypeWidget)
        return response