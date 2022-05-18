from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rarev2api.models import Tag


class TagView(ViewSet):
    """RareV2 Tag View"""
    
    def retrieve(self, request, pk):
        """Handles GET requests for a single tag"""
        
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) # INSQ how is ex.args[0] working?
    
    def list(self, request):
        """Handles GET requests for tags

        Args:
            request (HTTP): the Client's HTTP request
        """
        tags = Tag.objects.all().order_by('label')
        serializer = TagSerializer(tags, many=True)
        
        return Response(serializer.data)
    
    def create(self, request):
        """Handles POST requests for tags"""
        
        serializer = CreateTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        """Handles DELETE requests for tags
        
        Args:
            request (DELETE): Deletes selected event
            pk (primary key): The id of the tag to be deleted
            
        """
        
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk):
        """Handles PUT requests for tags
        
        Args:
            request (PUT): The HTTP PUT request from the client
            pk (primary key): The id of the tag to be edited
        """
        
        tag = Tag.objects.get(pk=pk)
        serializer = CreateTagSerializer(tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    
    class Meta:
        model = Tag
        fields = ('id', 'label')
        

class CreateTagSerializer(serializers.ModelSerializer):
    """JSON serializer for creating tags"""
    
    class Meta:
        model = Tag
        fields = ('id', 'label')