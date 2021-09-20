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


class KeywordSerializer(serializers.ModelSerializer):
    """JSON serializer for keywords
    Arguments: serializer type
    """
    class Meta:
        model = Keyword
        fields = '__all__'
