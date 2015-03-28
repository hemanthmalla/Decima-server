from rest_framework import serializers

from rest_api.models import *


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