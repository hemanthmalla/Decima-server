import logging
import json
import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_api.serializers import *

logger = logging.getLogger(__name__)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def createUser(request):
    logger.debug(request.body)
    json_data = json.loads(request.body)
    serializer = UserSerializer(data=json_data)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data, status=201)
    return JSONResponse(serializer.errors, status=400)


def decimaMail(request, key):
    decima = DecimaQuestions.objects.get(key=key)
    model = {"decima": decima}
    if decima.status == False:
        return render_to_response("allreadysubmitted.html", model, RequestContext(request))

    if request.method == "POST":
        option = request.POST.get("option")
        option = Option.objects.get(id=int(option))
        vote = Vote()
        vote.user_id = decima.user
        vote.question = decima.question
        vote.voted = True
        vote.option = option
        vote.save()
        decima.status = False
        decima.save()
        return render_to_response("successful.html", model, RequestContext(request))
    return render_to_response("decimaQuestionForm.html", model, RequestContext(request))


@csrf_exempt
def getContactsInNetwork(request):
    logger.debug(request.body)
    json_data = json.loads(request.body)
    user_contacts = json_data["contacts"]
    users_in_network = User.objects.filter(phone__in=user_contacts)
    serializer = UserSerializer(users_in_network, many=True)
    return JSONResponse(serializer.data)


@csrf_exempt
def makeDecision(request):
    logger.debug(request.body)
    json_data = json.loads(request.body)
    user_id = json_data["user_id"]
    options = json_data["options"]
    asked_to = json_data["asked_to"]
    question = Question(statement=json_data["question"], date_time_asked=datetime.datetime.now(),
                        asked_by=User.objects.get(id=user_id))
    question.save()
    for i in options:
        option = Option(name=i, quest_id=question.id)
        option.save()
        question.options.add(option)
    for i in asked_to:
        vote = Vote(user_id=User.objects.get(phone=i), question=question)
        vote.save()
    serializer = QuestionSerializer(question)
    return JSONResponse(serializer.data)


@csrf_exempt
def getQuestionsByUser(request):
    logger.debug(request.body)
    json_data = json.loads(request.body)
    user_id = json_data["user_id"]
    # this query set gets questions asked by the user
    queryset1 = Question.objects.filter(asked_by__id=user_id)
    # this query set gets questions this user has been asked to answer.
    # IMP TO-Do : this query needs to be rewritten using intermdeiate model - Vote
    queryset2 = Question.objects.filter(answers_by__id=user_id)  # doesn't work
    serializer = QuestionSerializer(queryset1 | queryset2, many=True)
    return JSONResponse(serializer.data)


@csrf_exempt
def getQuestionById(request):
    logger.debug(request.body)
    json_data = json.loads(request.body)
    quest_id = json_data["quest_id"]
    serializer = QuestionSerializer(Question.objects.get(id=quest_id))
    return JSONResponse(serializer.data)