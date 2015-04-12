from rest_framework import serializers
import logging
from rest_api.models import *

logger = logging.getLogger(__name__)
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class UserSerializerSecure(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote


class QuestionSerializer(serializers.ModelSerializer):
    has_voted = serializers.SerializerMethodField()
    asked_by = UserSerializerSecure()
    answers_by = UserSerializerSecure(many=True)
    def get_has_voted(self, obj):
        user = self.context.get("user_id")
        logger.debug(user)
        return Vote.objects.get(user_id_id=user, question=obj).voted

    class Meta():
        model = Question
        depth = 1