"""View module for handling requests about posts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rarev2api.models import Post
from rarev2api.models import RareUser
from django.db.models import Q 
from django.contrib.auth.models import User

class PostView(ViewSet):
    """Rare post view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        
        post = Post.objects.get(pk = pk)
        
        
        
        
        
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
        order_by_category = self.request.query_params.get('category', None)
        order_by_tag = self.request.query_params.get('tag_id', None)
        search_text_title = self.request.query_params.get('title', None)
        posts = Post.objects.all()
        if order_by_category is not None:
            # use the order by function to sort the posts
            # instead of using order by to exclude posts that dont have specific category id
            posts = Post.objects.filter(category__id=order_by_category)
        elif order_by_tag is not None:
            # use the order by function to sort the posts
            posts = Post.objects.filter(tags__id=order_by_tag)
        else:
            # other wise return all the posts
            # we run this second to make sure we can sort the posts on page load
            posts = Post.objects.all()
        if search_text_title is not None:
            # filter the game titles, descripts, and/or designers that contain our text from param
            posts = Post.objects.filter(
                Q(title__contains=search_text_title)
            )
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff')
        
class RareUserSerializer(serializers.ModelSerializer):
    user= UserSerializer()
    
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'active', 'user')
        depth = 1  
                
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    user = RareUserSerializer()
    class Meta:
        model = Post
        fields = ('id', 'user','category','title','publication_date','image_url','content','approved','tags', 'comments')
        depth =  1

class CreatePostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ('id', 'category','title','publication_date','image_url','content','approved','tags')
    