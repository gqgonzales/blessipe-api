"""View module for handling requests about recipes"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.db.models import Case, When
from django.db.models.fields import BooleanField
from blessipeapi.models import Recipe, Traveler, RecipeImage
from django.contrib.auth.models import User
import uuid


class RecipeImageView(ViewSet):
    """Blessipe images!"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized image instance
        """

        traveler = Traveler.objects.get(user=request.auth.user)
        recipe_image = RecipeImage()

        # Create a new instance of the game picture model you defined
        # Example: recipe_image = RecipeImage()
        format, imgstr = request.data["image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),
                           name=f'{request.data["recipe_id"]}-{uuid.uuid4()}.{ext}')

        # Give the image property of your recipe picture instance a value
        # For example, if you named your property `action_pic`, then
        # you would specify the following code:
        #
        #       game_picture.action_pic = data

        # Save the data to the database with the save() method

        recipe_image.traveler = traveler
        recipe_image.image = data

        recipe = Recipe.objects.get(pk=request.data["recipe"])
        recipe_image.recipe = recipe

        try:
            recipe_image.save()
            serializer = RecipeImageSerializer(
                recipe, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for an image

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            recipe_image = RecipeImage.objects.get(pk=pk)
            recipe_image.delete()

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
        recipe_images = RecipeImage.objects.all()

        serializer = RecipeImageSerializer(
            recipe_images, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single image

        Returns:
            Response -- JSON serialized image instance
        """
        try:
            recipe_image = RecipeImage.objects.get(pk=pk)
            serializer = RecipeImageSerializer(
                recipe_image, context={'request': request})
            return Response(serializer.data)
        except RecipeImage.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)


class RecipeImageSerializer(serializers.ModelSerializer):
    """JSON serializer for images

    Arguments:
        serializer type
    """
    class Meta:
        model = Recipe
        fields = ('id', 'image', 'recipe', 'traveler')
        depth = 1
