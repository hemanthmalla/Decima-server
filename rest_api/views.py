import logging
import json
import datetime
import urllib
from django.utils.text import slugify

from gcm import GCM
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import sleekxmpp
from rest_api.forms import OptionForm, QuestionForm
from rest_api.serializers import *
from django.conf import settings

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
    if User.objects.filter(phone=json_data["phone"]).__len__() == 0:
        serializer = UserSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        logger.debug(serializer.errors)
        return JSONResponse(serializer.errors, status=400)
    else:
        return HttpResponse(status=400)


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
        option.votes += 1
        option.save()
        decima.save()
        return render_to_response("successful.html", model, RequestContext(request))
    return render_to_response("decimaQuestionForm.html", model, RequestContext(request))


@csrf_exempt
def submit_vote(request):
    json_data = json.loads(request.body)
    question = int(json_data["question"])
    option_id = int(json_data["option"])
    user_id = int(json_data["user"])
    try:
        vote = Vote.objects.get(question_id=question, user_id_id=user_id)
        if vote.voted == True:
            return JSONResponse({}, status=status.HTTP_400_BAD_REQUEST)
    except Vote.DoesNotExist:
        pass
    question_obj = Question.objects.get(id=question)
    option_obj = Option.objects.get(id=option_id)
    user_obj = User.objects.get(id=user_id)
    vote = Vote.objects.get(user_id=user_obj, question=question_obj)
    vote.voted = True
    vote.option = option_obj
    vote.save()
    option = Option.objects.get(id=option_id)
    option.votes += 1
    option.save()
    return JsonResponse({}, status=status.HTTP_200_OK)


@csrf_exempt
def getContactsInNetwork(request):
    logger.debug(request.body)
    json_data = json.loads(request.body)
    user_contacts = json_data["contacts"]
    users_in_network = User.objects.filter(phone__in=user_contacts)
    serializer = UserSerializerSecure(users_in_network, many=True)
    return JSONResponse(serializer.data)


@csrf_exempt
def makeDecision(request):
    logger.debug(request.body)
    json_data = json.loads(request.body)
    user_id = json_data["user_id"]
    options = json_data["options"]
    asked_to = json_data["asked_to"]
    asked_by_user = User.objects.get(id=user_id)
    question = Question(statement=json_data["question"], date_time_asked=datetime.datetime.now(),
                        asked_by=asked_by_user)
    question.save()
    self_vote = Vote(user_id=asked_by_user, question=question)
    self_vote.save()
    for i in options:
        option = Option(name=i, quest_id=question.id)
        option.save()
        question.options.add(option)
    gcm_ids = []
    for i in asked_to:
        user = User.objects.get(phone=i)
        vote = Vote(user_id=user, question=question)
        vote.save()
        gcm_ids.append(user.gcm_id)
    gcm = GCM(settings.GCM_API_KEY)
    data = {"action": "Requesting your Opinion"}
    gcm_status = gcm.json_request(registration_ids=gcm_ids, data=data)
    logger.debug(gcm_status)
    serializer = QuestionSerializer(question)
    return JSONResponse(serializer.data)


@csrf_exempt
def getQuestionsByUser(request):
    logger.debug(request.body)
    json_data = json.loads(request.body)
    user_id = json_data["user_id"]
    # this query set gets questions asked by the user
    queryset1 = Question.objects.filter(asked_by_id=user_id)
    # this query set gets questions this user has been asked to answer.
    # IMP TO-Do : this query needs to be rewritten using intermdeiate model - Vote
    queryset2 = Question.objects.filter(
        id__in=Vote.objects.filter(user_id_id=user_id).values_list('question', flat=True))
    # queryset2 = Question.objects.filter(id__in=Vote.objects.filter(user_id_id=user_id))
    serializer = QuestionSerializer(queryset1 | queryset2, many=True, context={'user_id': user_id})
    return JSONResponse(serializer.data)


@csrf_exempt
def getQuestionById(request):
    logger.debug(request.body)
    json_data = json.loads(request.body)
    quest_id = json_data["quest_id"]
    serializer = QuestionSerializer(Question.objects.get(id=quest_id))
    return JSONResponse(serializer.data)


@csrf_exempt
@api_view(["GET", "POST"])
def question_invite(request):
    model = {}
    json_data = json.loads(request.body)
    question = Question.objects.get(id=int(json_data.get("group_id")))
    model["question"] = question
    model["users"] = User.objects.filter(phone__in=json_data.get("user_ids"))
    if request.method == "POST":
        for user in model["users"]:
            question.peers_involved.add(user)
            vote = Vote(user_id=user, question=question)
            vote.save()
        gcm_ids = [user.gcm_id for user in model["users"]]
        gcm = GCM(settings.GCM_API_KEY)
        data = {"action": "invite", "msg":"Can you help me decide what to buy?"}
        gcm_status = gcm.json_request(registration_ids=gcm_ids, data=data)
        logger.debug(gcm_status)
        question.is_active = True
        question.save()
        return Response({}, status=status.HTTP_200_OK)
    return render_to_response('question_invite.html', model, RequestContext(request))


@csrf_exempt
@api_view(["GET", "POST", ])
def msg_text(request):
    json_data = json.loads(request.body)
    msg = json_data.get("msg")
    group_id = json_data.get("group_id")
    group = Question.objects.get(id=group_id)
    if request.method == "POST":
        peers_involved = group.peers_involved.all()
        if peers_involved:
            gcm_ids = [peer.gcm_id for peer in peers_involved]
            gcm = GCM(settings.GCM_API_KEY)
            data = {"action": "chat", "msg": msg}
            gcm_status = gcm.json_request(registration_ids=gcm_ids, data=data)
        return Response({}, status=status.HTTP_200_OK)


def add_option(request, key):
    model = {}
    question = Question.objects.get(id=int(key))
    model["question"] = question
    option_form = OptionForm(request.POST or None)
    if request.method == "POST" and option_form.is_valid():
        option = option_form.save(commit=False)
        option.quest_id = question.id
        option.save()
        question.options.add(option)
        question.save()
        return redirect(question.get_add_option_url())
    model["form"] = option_form
    return render_to_response('add_option.html', model, RequestContext(request))


def decimo(request, key):
    model = {}
    question = Question.objects.get(id=int(key))
    model["question"] = question
    return render_to_response('decimo.html', model, RequestContext(request))


def decimo_question(request, key):
    model = {}
    question = Question.objects.get(id=int(key))
    model["question"] = question
    decima = DecimaQuestions()
    decima.question = question
    model["decima"] = decima
    return render_to_response('decimo_question.html', model, RequestContext(request))


def create_question(request):
    model = {}
    question_form = QuestionForm(request.POST or None)
    if request.method == "POST" and question_form.is_valid():
        question = question_form.save(commit=False)
        question.asked_by_id = 1
        question.save()
        return redirect(question.get_add_option_url())
    model["form"] = question_form
    return render_to_response('create_question.html', model, RequestContext(request))


def get_myntra_product_details(pid):
    try:
        return Products.objects.get(identifier=pid)
    except Products.DoesNotExist:
        pass

    pr = Products()
    url = "http://developer.myntra.com/style/%s" % pid
    obj = json.loads(urllib.urlopen(url).read()).get("data", {})
    pr.title = obj.get("productDisplayName")
    pr.final_price = obj.get("discountedPrice")
    pr.item_price = obj.get("price")
    pr.discount_percent = ((pr.item_price - pr.final_price) * 100) / pr.item_price
    pr.source = obj.get("landingPageUrl")
    pr.image = obj.get("styleImages").get("default").get("imageURL")
    pr.identifier = pid
    pr.save()
    return pr


@csrf_exempt
@api_view(["GET", "POST"])
def post_product(request):
    json_data = json.loads(request.body)
    user_id = json_data["user_id"]
    pid = json_data["product_id"]
    pr = get_myntra_product_details(pid)
    if json_data.get("group_id", None):
        question = Question.objects.get(id=int(json_data.get("group_id")))
    else:
        question = Question()
        question.statement = "What's there in a name?"
        if json_data.get("title",None):
            question.statement = json_data.get("title")
        question.is_active = False
        question.asked_by_id = user_id
        question.save()
        self_vote = Vote(user_id=User.objects.get(id=int(user_id)), question=question)
        self_vote.save()
    question.products.add(pr)
    question.save()
    return Response({"user_id": user_id, "group": QuestionSerializer(question).data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def index_controller(request):
    return Response(QuestionSerializer(Question.objects.all().order_by("-date_time_asked"), many=True).data,
                    status=status.HTTP_200_OK)


def start_decision_controller(request):
    model = {}
    model["contacts"] = User.objects.all()
    return render_to_response('start_decision_controller.html', model)