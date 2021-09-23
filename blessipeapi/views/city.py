"""View module for handling requests about cities"""
from django.core.exceptions import ValidationError
from rest_framework import permissions, status
from django.http import HttpResponseServerError
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from blessipeapi.models import City, Country


class CityView(ViewSet):
    """Blessipe city viewset"""

    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """Handle GET requests to cities resource

            Returns:
                Response -- JSON serialized list of cities
            """
        # Get all city records from the database
        cities = City.objects.all()

        serializer = CitySerializer(
            cities, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized city instance
        """
        # Create a new Python instance of the City class
        # and set its properties from what was sent in the
        # body of the request from the client.
        city = City()
        city.name = request.data["name"]

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `restaurant_id` in the body of the request.
        country = Country.objects.get(pk=request.data["country"])
        city.country = country

        # Try to save the new city to the database, then
        # serialize the city instance as JSON, and send the
        # JSON as a response to the client request
        try:
            city.save()
            serializer = CitySerializer(
                city, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single city

        Returns:
            Response -- JSON serialized city instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/cities/2
            #
            # The `2` at the end of the route becomes `pk`
            city = City.objects.get(pk=pk)
            serializer = CitySerializer(
                city, context={'request': request})
            return Response(serializer.data)
        except City.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a city

        Returns:
            Response -- Empty body with 204 status code
        """
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of City, get the city record
        # from the database whose primary key is `pk`
        city = City.objects.get(pk=pk)
        city.name = request.data["name"]
        city.country = Country.objects.get(pk=request.data["country"])
        city.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single city

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            city = City.objects.get(pk=pk)
            city.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except City.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CitySerializer(serializers.ModelSerializer):
    """JSON serializer for cities

    Arguments:
        serializer type
    """
    class Meta:
        model = City
        fields = ('id', 'name', 'country')
        depth = 1
