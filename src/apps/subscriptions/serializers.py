

from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated

class SubscriptionSerializer(serializers.Serializer):