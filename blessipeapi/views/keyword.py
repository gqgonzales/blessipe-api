"""View module for handling keyword requests"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from blessipeapi.models import Keyword


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


class KeywordSerializer(serializers.ModelSerializer):
    """JSON serializer for keywords
    Arguments: serializer type
    """
    class Meta:
        model = Keyword
        fields = '__all__'
