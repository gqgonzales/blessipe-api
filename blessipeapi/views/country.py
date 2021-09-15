"""View module for handling requests about countries"""
from django.core.exceptions import ValidationError
from django.views.generic.base import View
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from blessipeapi.models import Country


class CountryView(ViewSet):
    """Our lovely list of countries"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized country instance
        """

        country = Country()
        country.name = request.data["name"]

        try:
            country.save()
            serializer = CountrySerializer(
                country, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single country

        Returns:
            Response -- JSON serialized country instance
        """
        try:
            country = Country.objects.get(pk=pk)
            serializer = CountrySerializer(
                country, context={'request': request})
            return Response(serializer.data)
        except Country.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a country

        Returns:
            Response -- Empty body with 204 status code
        """

        country = Country.objects.get(pk=pk)
        country.name = request.data["name"]

        country.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single country

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            country = Country.objects.get(pk=pk)
            country.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Country.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to countries resource

        Returns:
            Response -- JSON serialized list of countries
        """
        countries = Country.objects.all()

        serializer = CountrySerializer(
            countries, many=True, context={'request': request})
        return Response(serializer.data)


class CountrySerializer(serializers.ModelSerializer):
    """JSON serializer for countries

    Arguments:
        serializer type
    """
    class Meta:
        model = Country
        fields = ('id', 'name')
        depth = 1
