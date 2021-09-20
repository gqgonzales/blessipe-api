"""View module for handling keyword requests"""
from blessipeapi.models.restaurant import Restaurant
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from blessipeapi.models import RestaurantKeyword, Keyword, Restaurant


class RestaurantKeywordView(ViewSet):
    """Restaurant Keywords"""

    def list(self, request):
        """Handle GET requests to restaurant_keywords resource
        Returns:
            Response -- JSON serialized list of restaurant_keywords
        """

        restaurant_keywords = RestaurantKeyword.objects.all()

        restaurant = self.request.query_params.get('restaurant', None)
        if restaurant is not None:
            restaurant_keywords = restaurant_keywords.filter(
                restaurant__id=restaurant)
        #  This dunderscored id is acting kind of like a join table WHERE statement

        serializer = RestaurantKeywordSerializer(
            restaurant_keywords, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single keyword

        Returns:
            Response -- JSON serialized keyword instance
        """
        try:
            keyword = RestaurantKeyword.objects.get(pk=pk)
            serializer = RestaurantKeywordSerializer(
                keyword, context={'request': request})
            return Response(serializer.data)
        except RestaurantKeyword.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(methods=['post'], detail=True)
    def add_restaurant_keyword(self, request, pk=None):
        """Add a keyword to the the database, then a specified restaurant"""
        keyword = Keyword()
        keyword.word = request.data["word"]

        try:

            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response(
                {'message': 'Restaurant does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == "POST":
            try:
                keyword.save()
                restaurant.keywords.add(keyword)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})


class RestaurantSerializer(serializers.ModelSerializer):
    """Relevant restaurant data to be returned"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name')
        depth = 1


class RestaurantKeywordSerializer(serializers.ModelSerializer):
    """JSON serializer for restaurant_keywords
    Arguments: serializer type
    """

    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = RestaurantKeyword
        fields = '__all__'
        depth = 1
