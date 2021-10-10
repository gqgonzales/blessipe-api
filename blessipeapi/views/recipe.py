"""View module for handling requests about recipes"""
from django.core.files.base import ContentFile
import base64
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
from blessipeapi.models import Recipe, Traveler, Restaurant, RecipeKeyword, Keyword, City
from blessipeapi.views.restaurant import RestaurantSerializer
from django.contrib.auth.models import User
import uuid


class RecipeView(ViewSet):
    """Blessipe recipes"""

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
        recipe.is_public = request.data["isPublic"]
        recipe.traveler = traveler

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `restaurant` in the body of the request.
        restaurant = Restaurant.objects.get(pk=request.data["restaurant"])
        recipe.restaurant = restaurant
        if request.data["image"] != "":
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                               name=f'{uuid.uuid4()}.{ext}')
        else:
            data = None
        recipe.image = data

        # Try to save the new recipe to the database, then
        # serialize the recipe instance as JSON, and send the
        # JSON as a response to the client request
        try:
            recipe.save()
            # recipe.keywords.set([])

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
            # recipe = Recipe.objects.get(pk=pk)
            traveler = Traveler.objects.get(user=request.auth.user)
            recipe = Recipe.objects.annotate(
                author=Case(
                    When(traveler=traveler, then=True),
                    default=False,
                    output_field=BooleanField()
                )).get(pk=pk)

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
        recipe.is_public = request.data["isPublic"]

        recipe.traveler = traveler

        restaurant = Restaurant.objects.get(pk=request.data["restaurant"])
        recipe.restaurant = restaurant

        if request.data["image"] is not None:
            image_splitter = request.data["image"].split("/")
            if image_splitter[0] == "http:":
                pass
            else:
                format, imgstr = request.data["image"].split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr),
                                   name=f'{uuid.uuid4()}.{ext}')
                recipe.image = data
        else:
            recipe.image = None
        recipe.save()
        # recipe.keywords.set(request.data["keywords"])

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

        traveler = Traveler.objects.get(user=request.auth.user)
        recipes = Recipe.objects.annotate(
            author=Case(
                When(traveler=traveler, then=True),
                default=False,
                output_field=BooleanField()
            ))

        keywords = self.request.query_params.get('type', None)
        if keywords is not None:
            recipes = recipes.filter(keyword__id=keywords)

        serializer = RecipeSerializer(
            recipes, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def find_local_restaurants(self, request, pk=None):
        """Evaluate the words in the keyword list of the given recipe.
        Then, check the keywords in the lists of all restaurants
        If a restaurant has a keyword that is similar, return that list instead of all restaurants"""
        traveler = Traveler.objects.get(user=request.auth.user)

        if request.method == "GET":
            try:

                recipe = Recipe.objects.get(pk=pk)

                # Need to destructure list of current recipe's keyword list. Just want the strings.
                words = [kw.word for kw in recipe.keywords.all()]

                matched_results = Restaurant.objects.filter(
                    keywords__word__in=words,
                    city=traveler.city).distinct()

                for restaurant in matched_results:
                    restaurant.favorited = traveler in restaurant.super_fans.all()
                # matched_results.order_by(hits.annotate(
                #         count=Count('WHAT WERE SEARCHING FOR')))

                # Destructured list gets passed in to the __in filter, returning only restaurants with a match.
                # Lastly, filter the filtered list to return only restaurants in the city = traveler.city
                # Could you set a minimum match limit? Hannah says no.
                # Could we order_by() the number of successful matches?

                serializer = RestaurantSerializer(
                    matched_results, context={'request': request}, many=True)
                return Response(serializer.data)
            except Restaurant.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return HttpResponseServerError(ex)


class RecipeUserSerializer(serializers.ModelSerializer):
    """Not sure if this is really necessary, we'll see

    Arguments:
        serializer type
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        depth = 1


class RecipeTravelerSerializer(serializers.ModelSerializer):
    """Not sure if this is really necessary, we'll see

    Arguments:
        serializer type
    """

    user = RecipeUserSerializer(many=False)

    class Meta:
        model = Traveler
        fields = ('id', 'user', 'city')
        depth = 1


class CitySerializer(serializers.ModelSerializer):
    """Returns necessary city / country information"""
    class Meta:
        model = City
        fields = "__all__"
        depth = 1


class RecipeKeywordSerializer(serializers.ModelSerializer):
    """Return keywords on a recipe!"""

    model = RecipeKeyword
    fields = 'word'


class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for recipes

    Arguments:
        serializer type
    """

    traveler = RecipeTravelerSerializer(many=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'date',
                  'restaurant', 'traveler', 'author', 'is_public', 'image', 'keywords')
        depth = 2
