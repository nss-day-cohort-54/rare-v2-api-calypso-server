from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rarev2api.models import Tag

class TagView(ViewSet):
    """RareV2 Tag View"""
    
    def list(self, request):
        """Handles GET requests for tags

        Args:
            request (HTTP): the Client's HTTP request
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        
        return Response(serializer.data)
    
    def create(self, request):
        """Handles POST requests for tags"""
        
        serializer = CreateTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    
    class Meta:
        model = Tag
        fields = ('id', 'label')
        

class CreateTagSerializer(serializers.ModelSerializer):
    """JSON serializer for creating tags"""
    
    class Meta:
        model = Tagfields = ('id', 'label')