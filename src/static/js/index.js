//// History Class
function History(target, questionBoxTarget) {
    this.target = target;
    this.questionBoxTarget = questionBoxTarget;
    this.nohistory = true;
    this.target.html("<i>No history</i>");
}

History.prototype.Add = function (question) {
    var $this = this;
    var history = $("<div class=\"history\">" +question +"</div>");
    if (this.nohistory === true) {
        this.target.html(history);
        this.nohistory = false;
    } else {
        this.target.prepend(history);
    }

    history.on('click', function() {
        console.log($(this).html());
        $this.questionBoxTarget.val($(this).html());
        $this.questionBoxTarget.focus();
    });
}

//// Widget handler
function WidgetHandler(target) {
    this.target = target;
}

WidgetHandler.prototype.Clear = function() {
    this.target.html("");
}

WidgetHandler.prototype.GetWidget = function (question, widget, correlationid) {
    var htmlContent = "<div class='widget " +widget.widgetType +"'>";
    htmlContent += "<div class='header'>" +widget.key +"</div>";

    if (widget.displayContract == "text") {
        if (widget.value) {
            htmlContent += "<div class='body'>" +widget.value +"</div>";
        }

        if (widget.feedbackUrl && widget.feedbackUrl.trim() !== "") {
            htmlContent += "<div class='feedbacks' question='" 
                + question +"' correlationId='" 
                + correlationid +"' url='" 
                + widget.feedbackUrl +"' partAnswer='"
                + widget.value +"'>";

            htmlContent += "<a href='#feedback/" +correlationid +"/correct'>correct</a> / ";
            htmlContent += "<a href='#feedback/" +correlationid +"/incorrect'>incorrect</a>";
            htmlContent += "</div>";
        }
    } else if (widget.displayContract == "textarea") {
        htmlContent += "<textarea style='width: 100%;min-height: 100px' readonly>" +widget.value +"</textarea>";
    }

    htmlContent += "</div>"; 
    return htmlContent;  
}

WidgetHandler.prototype.Render = function(response, correlationid) {
    var question = response.result.question;
    var widgets = response.result.widgets;
    $this = this;
    this.Clear();
    widgets.forEach(function (widget) {
        $this.target.append($this.GetWidget(question, widget, correlationid));
    });

    $this.target.append(
        $this.GetWidget(
            question,
            {
                displayContract: "textarea",
                key: "Raw Response",
                value: JSON.stringify(response, null, '\t'),
                widgetType: "full"
            },
            correlationid))
}

//// Question Answer Handler Class Class
function QADebugger(target) {
    this.target = target;
    this.target.html(
        "<div class='question' id='qad_question'></div>"
        + "<div class='answer' id='qad_answer'></div>"
        + "<div class='widgets' id='qad_widgets'></div>");

    this.questionTarget = $("#qad_question");
    this.answerTarget = $("#qad_answer");
    this.widgetsTarget = new WidgetHandler($("#qad_widgets"));
}

QADebugger.prototype.Question = function(question) {
    //// ajax request
    var $this = this;
    var loading = "<img src='https://loading.io/spinners/cloudy/index.cloudy-sky-preloader.svg'></img>";
    this.questionTarget.html(question);
    this.answerTarget.html(loading);

    var payload = {
        question: question
    };

    $.ajax({
        url: '/api/v1/question',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            $this.answerTarget.html("<strong>Answer: </strong>" +data.result.answer);
            $this.widgetsTarget.Render(data, data.result.uuid);
        },
        data: JSON.stringify(payload)
    });
}

$(document).ready(function() {
    var history = new History($("#history_container"), $("#input_question"));
    var qaDebugger = new QADebugger($("#qaworkspace"))

    $('.history').on('click', function() {
        console.log($(this).html());
        $('#input_question').val($(this).html().trim());
        $('#input_submit').focus();
    });

    $('#input_submit').on('click', function() {
        var question = $('#input_question').val().trim();
        if (question && question.length > 0) {
            qaDebugger.Question(question);
            history.Add(question);
        };
    });

    $("#qad_widgets").on('click', '.feedbacks a', function(evt) {
        var $this = $(this);
        var question = $(this).parent().attr("question").trim();
        var partAnswer = $(this).parent().attr("partAnswer").trim();
        var url = $(this).parent().attr("url").trim();
        var correlationId = $(this).parent().attr("correlationId").trim();
        var value = $(this).html().trim();

        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                $this.parent().html("feedback submitted!");
            },
            data: JSON.stringify({
                correlationId: correlationId,
                value: value,
                question: question,
                partAnswer: partAnswer
            })
        });
        evt.stopPropagation();
        evt.preventDefault();
    });
});