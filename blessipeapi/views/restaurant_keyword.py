"""View module for handling keyword requests"""
from blessipeapi.models import restaurant
from blessipeapi.models.restaurant import Restaurant
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from blessipeapi.models import RestaurantKeyword


class RestaurantKeywordView(ViewSet):
    """Recipe Keywords"""

    def list(self, request):
        """Handle GET requests to recipe_keywords resource
        Returns:
            Response -- JSON serialized list of recipe_keywords
        """

        recipe_keywords = RestaurantKeyword.objects.all()

        serializer = RestaurantKeywordSerializer(
            recipe_keywords, many=True, context={'request': request})
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


class RestaurantSerializer(serializers.ModelSerializer):
    """Relevant restaurant data to be returned"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name')
        depth = 1


class RestaurantKeywordSerializer(serializers.ModelSerializer):
    """JSON serializer for recipe_keywords
    Arguments: serializer type
    """

    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = RestaurantKeyword
        fields = '__all__'
        depth = 1
