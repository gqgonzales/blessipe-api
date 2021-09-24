from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from blessipeapi.models import Traveler


class ProfileView(ViewSet):
    """To view profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and events
        """
        traveler = Traveler.objects.get(user=request.auth.user)
        profiles = Traveler.objects.all()

        user = self.request.query_params.get('userId', None)
        if user is not None:
            profiles = profiles.get(user__id=user)

            serializer = TravelSerializer(
                profiles, many=False, context={'request': request})
            return Response(serializer.data)
        else:
            traveler = TravelSerializer(
                traveler, many=False, context={'request': request})

            profile = {}
            profile["user"] = traveler.data

            return Response(profile)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer"""
    class Meta:
        model = User
        fields = ('username', 'email', 'date_joined',
                  'is_staff', 'first_name', 'last_name')


class TravelSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    user = UserSerializer(many=False)

    class Meta:
        model = Traveler
        fields = ('id', 'user', 'bio', 'full_name', 'city')
        depth = 1
