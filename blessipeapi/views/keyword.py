"""View module for handling keyword requests"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from blessipeapi.models import Keyword, Recipe
from rest_framework.decorators import action


class KeywordView(ViewSet):
    """General list of keywords"""

    def list(self, request):
        """Handle GET requests to keywords resource
        Returns:
            Response -- JSON serialized list of keywords
        """

        keywords = Keyword.objects.all()



        serializer = KeywordSerializer(
            keywords, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single keyword

        Returns:
            Response -- JSON serialized keyword instance
        """
        try:
            keyword = Keyword.objects.get(pk=pk)
            serializer = KeywordSerializer(
                keyword, context={'request': request})
            return Response(serializer.data)
        except Keyword.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized keyword instance
        """

        keyword = Keyword()
        keyword.word = request.data["word"]

        try:
            keyword.save()
            serializer = KeywordSerializer(
                keyword, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single keyword

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            keyword = Keyword.objects.get(pk=pk)
            keyword.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Keyword.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get', 'post'], detail=True)
    def add_keyword(self, request, pk=None):
        """Add a keyword to the database"""
    # Django uses the `Authorization` header to determine
    # which user is making the request to signup
        keyword = Keyword.objects.all()

        try:
            # Handle the case if the client specifies a recipe
            # that doesn't exist
            recipe = Recipe.objects.get(pk=pk)
            Keywords = Keyword()

        except Recipe.DoesNotExist:
            return Response(
                {'message': 'Recipe does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # A recipe wants to sign up for an recipe
        if request.method == "POST":
            try:
                # Using the keywords field on the recipe makes it simple to add a recipe to the recipe
                # .add(recipe) will insert into the join table a new row the gamer_id and the event_id
                Keywords.add(keyword)
                recipe.keywords.add(keyword)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})

        # User wants to leave a previously joined recipe
        elif request.method == "DELETE":
            try:
                # The many to many relationship has a .remove method that removes the recipe from the keywords list
                # The method deletes the row in the join table that has the gamer_id and event_id
                recipe.keywords.remove(keyword)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})


class KeywordSerializer(serializers.ModelSerializer):
    """JSON serializer for keywords
    Arguments: serializer type
    """
    class Meta:
        model = Keyword
        fields = '__all__'
