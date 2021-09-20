"""View module for handling keyword requests"""
from blessipeapi.models.recipe import Recipe
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from blessipeapi.models import RecipeKeyword, Keyword


class RecipeKeywordView(ViewSet):
    """Recipe Keywords"""

    def list(self, request):
        """Handle GET requests to recipe_keywords resource
        Returns:
            Response -- JSON serialized list of recipe_keywords
        """

        recipe_keywords = RecipeKeyword.objects.all()

        # Support filtering keywords by recipe
        #    http://localhost:8000/recipekeywords?recipe=1
        #
        # That URL will retrieve all keywords
        recipe = self.request.query_params.get('recipe', None)
        if recipe is not None:
            recipe_keywords = recipe_keywords.filter(recipe__id=recipe)
        #  This dunderscored id is acting kind of like a join table WHERE statement

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


class RecipeSerializer(serializers.ModelSerializer):
    """Only return specific recipe data from request"""

    class Meta:
        model = Recipe
        fields = ('id', 'name')


class RecipeKeywordSerializer(serializers.ModelSerializer):
    """JSON serializer for recipe_keywords
    Arguments: serializer type
    """

    recipe = RecipeSerializer(many=False)

    class Meta:
        model = RecipeKeyword
        fields = '__all__'
        depth = 1
