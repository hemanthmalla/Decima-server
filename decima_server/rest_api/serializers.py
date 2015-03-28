from decima_server.rest_api.models import *
from rest_framework import serializers


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        depth = 1