"""View module for handling keyword requests"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from blessipeapi.models import RecipeKeyword


class RecipeKeywordView(ViewSet):
    """Recipe Keywords"""

    def list(self, request):
        """Handle GET requests to recipe_keywords resource
        Returns:
            Response -- JSON serialized list of recipe_keywords
        """

        recipe_keywords = RecipeKeyword.objects.all()

        serializer = RecipeKeywordSerializer(
            recipe_keywords, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single keyword

        Returns:
            Response -- JSON serialized keyword instance
        """
        try:
            keyword = RecipeKeyword.objects.get(pk=pk)
            serializer = RecipeKeywordSerializer(
                keyword, context={'request': request})
            return Response(serializer.data)
        except RecipeKeyword.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)


class RecipeKeywordSerializer(serializers.ModelSerializer):
    """JSON serializer for recipe_keywords
    Arguments: serializer type
    """
    class Meta:
        model = RecipeKeyword
        fields = '__all__'
        depth = 1
