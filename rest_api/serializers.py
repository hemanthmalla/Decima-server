from rest_framework import serializers

from rest_api.models import *


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote


class QuestionSerializer(serializers.ModelSerializer):
    has_voted = serializers.SerializerMethodField()
    asked_by = UserSerializer()
    answers_by = UserSerializer(many=True)
    def get_has_voted(self, obj):
        return Vote.objects.get(user_id=obj.asked_by,question=obj).voted

    class Meta():
        model = Question
        depth = 1