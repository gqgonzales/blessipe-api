"""View module for handling requests travelers"""
from django.contrib.auth.models import User
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from blessipeapi.models.traveler import Traveler


class TravelerView(ViewSet):
    """To see traveler specific information"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single traveler
        Returns:
            Response -- JSON serialized traveler instance
        """
        try:
            user = Traveler.objects.get(pk=pk)
            serializer = TravelerSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and events
        """
        users = Traveler.objects.all()

        serializer = TravelerSerializer(
            users, many=True, context={'request': request})

        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Traveler's related Django user"""
    class Meta:
        model = User
        fields = ('is_staff', )


class TravelerSerializer(serializers.ModelSerializer):
    """post user serializer"""
    user = UserSerializer(many=False)

    class Meta:
        model = Traveler
        fields = ['id', 'full_name', 'user', 'bio']
