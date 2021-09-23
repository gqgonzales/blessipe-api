"""View module for handling requests about restaurants"""
from blessipeapi.models import city
from blessipeapi.models.city import City
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Case, When
from django.db.models.fields import BooleanField
from blessipeapi.views.traveler import TravelerSerializer
from blessipeapi.views.city import CitySerializer
from blessipeapi.models import Restaurant, Traveler, City, RestaurantKeyword, restaurant, traveler, Favorite


class RestaurantView(ViewSet):
    """Blessipe restaurant viewset"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized restaurant instance
        """
        # Create a new Python instance of the Restaurant class
        # and set its properties from what was sent in the
        # body of the request from the client.
        restaurant = Restaurant()
        restaurant.name = request.data["name"]
        restaurant.address = request.data["address"]
        restaurant.phone_number = request.data["phone_number"]
        restaurant.url = request.data["url"]

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `restaurant_id` in the body of the request.
        city = City.objects.get(pk=request.data["city"])
        restaurant.city = city

        # Try to save the new restaurant to the database, then
        # serialize the restaurant instance as JSON, and send the
        # JSON as a response to the client request
        try:
            restaurant.save()
            serializer = RestaurantSerializer(
                restaurant, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single restaurant

        Returns:
            Response -- JSON serialized restaurant instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/restaurants/2
            #
            # The `2` at the end of the route becomes `pk`
            restaurant = Restaurant.objects.get(pk=pk)
            serializer = RestaurantSerializer(
                restaurant, context={'request': request})
            return Response(serializer.data)
        except Restaurant.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a restaurant

        Returns:
            Response -- Empty body with 204 status code
        """
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Restaurant, get the restaurant record
        # from the database whose primary key is `pk`
        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.name = request.data["name"]
        restaurant.address = request.data["address"]
        restaurant.phone_number = request.data["phone_number"]
        restaurant.url = request.data["url"]
        restaurant.city = City.objects.get(pk=request.data["city"])
        restaurant.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single restaurant

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            restaurant.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Restaurant.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to restaurants resource

        Returns:
            Response -- JSON serialized list of restaurants
        """
        traveler = Traveler.objects.get(user=request.auth.user)
        restaurants = Restaurant.objects.all()

        for restaurant in restaurants:
            restaurant.favorited = traveler in restaurant.super_fans.all()

        keywords = self.request.query_params.get('type', None)
        if keywords is not None:
            restaurants = restaurants.filter(keyword__id=keywords)

        serializer = RestaurantSerializer(
            restaurants, many=True, context={'request': request})
        return Response(serializer.data)

    @ action(methods=['post', 'delete'], detail=True)
    def favorite_restaurant(self, request, pk=None):
        """Managing favoriting a restaurant"""
        traveler = Traveler.objects.get(user=request.auth.user)

        try:
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response(
                {'message': 'Restaurant does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == "POST":
            try:
                restaurant.super_fans.add(traveler)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})

        # User wants to unfavorite a restaurant
        elif request.method == "DELETE":
            try:
                restaurant.super_fans.remove(traveler)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})

    # @ action(methods=['get'], detail=True)
    # def favorites(self, request, pk=None):
    #     """Only return restaurants that have been favorited by current traveler"""

    #     if request.method == "GET":
    #         try:
    #             traveler = Traveler.objects.get(user=request.auth.user, pk=pk)

    #             restaurants = Restaurant.objects.all()

    #             favorites_list = Favorite.objects.filter(traveler=traveler)
    #             if len(favorites_list) > 0:
    #                 for favorites in favorites_list:
    #                     restaurants = Restaurant.objects.filter(
    #                         pk=favorites.restaurant.id)

                # restaurants = restaurants.filter()

                # for restaurant in restaurants:

                #     restaurant.favorited = traveler in restaurant.super_fans.all()

                #         only_favorites = Restaurant.objects.filter()

                # for restaurant in restaurants:
                #     restaurant.favorited = traveler in restaurant.super_fans.all()

                # restaurants = Restaurant.objects.filter(favorited=True)

                # restaurants = Restaurant.objects.annotate(
                #     favorited=traveler in restaurant.super_fans.all()).filter(favorited=True)

        #     except Restaurant.DoesNotExist:
        #         return Response(
        #             {'message': 'Restaurant does not exist.'},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )

        # serializer = RestaurantSerializer(
        #     restaurants, many=True, context={'request': request})
        # return Response(serializer.data)
# The serializer class determines how the Python data should be serialized as JSON to be sent back to the client.


class RestaurantKeywordSerializer(serializers.ModelSerializer):
    """Return keywords on a recipe!"""

    model = RestaurantKeyword
    fields = 'word'


class CitySerializer(serializers.ModelSerializer):
    """Returns necessary city / country information"""
    class Meta:
        model = City
        fields = "__all__"
        depth = 1


class RestaurantSerializer(serializers.ModelSerializer):
    """JSON serializer for restaurants

    Arguments:
        serializer type
    """

    city = CitySerializer(many=False)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'phone_number',
                  'url', 'city', 'keywords', 'super_fans', 'favorited')
        depth = 1
