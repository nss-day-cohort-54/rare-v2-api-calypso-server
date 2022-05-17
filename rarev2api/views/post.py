"""View module for handling requests about posts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rarev2api.models import Post
from rarev2api.models import RareUser

class PostView(ViewSet):
    """Rare post view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST requests

        Returns:
            Response -- JSON serialized post
        """
        user = RareUser.objects.get(user=request.auth.user)
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests

        Returns:
            Response -- 204 No Content status code
        """
        post = Post.objects.get(pk=pk)
        serializer = CreatePostSerializer(post, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Handle DELETE requests

        Args:
            Return -- 204 No Content status code
        """
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
                
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ('id', 'user','category','title','publication_date','image_url','content','approved','tags')
        depth =  1

class CreatePostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ('category','title','publication_date','image_url','content','approved','tags')
    