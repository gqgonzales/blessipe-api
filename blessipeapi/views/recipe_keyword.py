"""View module for handling keyword requests"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from blessipeapi.models import RecipeKeyword, Keyword, Recipe


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

    @action(methods=['post'], detail=True)
    def add_recipe_keyword(self, request, pk=None):
        """Add a keyword to the the database, then a specified recipe"""
        keyword = Keyword()
        keyword.word = request.data["word"]

        try:

            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response(
                {'message': 'Recipe does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == "POST":
            try:
                keyword.save()
                recipe.keywords.add(keyword)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})


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
