"""View module for handling requests about recipes"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from blessipeapi.models import Recipe, Traveler, Restaurant


class RecipeView(ViewSet):
    """Level up recipes"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized recipe instance
        """

        # Uses the token passed in the `Authorization` header
        traveler = Traveler.objects.get(user=request.auth.user)

        # Create a new Python instance of the Recipe class
        # and set its properties from what was sent in the
        # body of the request from the client.
        recipe = Recipe()
        recipe.name = request.data["name"]
        recipe.description = request.data["description"]
        recipe.date = request.data["date"]
        recipe.traveler = traveler

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `restaurant_id` in the body of the request.
        restaurant = Restaurant.objects.get(pk=request.data["restaurant_id"])
        recipe.restaurant = restaurant

        # Try to save the new recipe to the database, then
        # serialize the recipe instance as JSON, and send the
        # JSON as a response to the client request
        try:
            recipe.save()
            serializer = RecipeSerializer(recipe, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single recipe

        Returns:
            Response -- JSON serialized recipe instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/recipes/2
            #
            # The `2` at the end of the route becomes `pk`
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe, context={'request': request})
            return Response(serializer.data)
        except Recipe.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a recipe

        Returns:
            Response -- Empty body with 204 status code
        """
        traveler = Traveler.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Recipe, get the recipe record
        # from the database whose primary key is `pk`
        recipe = Recipe.objects.get(pk=pk)
        recipe.name = request.data["name"]
        recipe.description = request.data["description"]
        recipe.date = request.data["date"]
        recipe.traveler = traveler

        restaurant = Restaurant.objects.get(pk=request.data["restaurant_id"])
        recipe.restaurant = restaurant
        recipe.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single recipe

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            recipe = Recipe.objects.get(pk=pk)
            recipe.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Recipe.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to recipes resource

        Returns:
            Response -- JSON serialized list of recipes
        """
        # Get all recipe records from the database
        recipes = Recipe.objects.all()

        # Support filtering recipes by traveler
        #    http://localhost:8000/recipes?traveler=1
        #
        # That URL will retrieve all tabletop recipes
        # traveler = self.request.query_params.get('traveler', None)
        # if traveler is not None:
        #     recipes = recipes.filter(traveler__id=traveler)
        #  This dunderscored id is acting kind of like a join table WHERE statement

        serializer = RecipeSerializer(
            recipes, many=True, context={'request': request})
        return Response(serializer.data)

# The serializer class determines how the Python data should be serialized as JSON to be sent back to the client.


class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for recipes

    Arguments:
        serializer type
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'date',
                  'restaurant', 'traveler')
        depth = 2
