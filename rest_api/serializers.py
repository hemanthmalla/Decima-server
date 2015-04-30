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


class ProductSerializer(serializers.ModelSerializer):
    product_link = serializers.SerializerMethodField()

    def get_product_link(self, obj):
        return "http://www.myntra.com/%s" % obj.source

    class Meta:
        model = Products


class QuestionSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Question
