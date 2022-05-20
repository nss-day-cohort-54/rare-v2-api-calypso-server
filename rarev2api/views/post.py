"""View module for handling requests about posts"""
from datetime import datetime
from operator import itemgetter, truediv
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from rarev2api.models import Post
from rarev2api.models import RareUser
from django.db.models import Q
from rest_framework.decorators import action
from rarev2api.models.comment import Comment
from rarev2api.models.tag import Tag
from rarev2api.views.comment import CommentSerializer 
from django.contrib.auth.models import User

class PostView(ViewSet):
    """Rare post view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single post
        
        Returns:
            Response -- JSON serialized post
        """
        
        try:
            # get all comments that have matching post id and order them by newest to oldest (- before makes them descending)
            comments = Comment.objects.filter(post = pk).order_by('-created_on')
            for comment in comments:
                if comment.author.user == request.auth.user:
                    print("true")
                    comment.is_user = True
                else:
                    print("false")
                    comment.is_user = False
            comments = CommentSerializer(comments, many = True)
            
            post = Post.objects.get(pk = pk)
            if post.user.user == request.auth.user:
                post.is_user = True
            serializer = PostSerializer(post)
            post.comments = comments.data

            serializer.data['comments'] = comments.data
            
            
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        get_by_user = self.request.query_params.get('user_id', None)
        if get_by_user is not None:
            posts = Post.objects.filter(user_id=get_by_user)
        else:
            # what is the 'none' value in query param tuple
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
    
    # we create a custom action method to get posts that belong to the logged in user
    # set our method to get to retrieve data and our detail to false to return a list instead of single object
    @action(methods=["get"], detail=False)
    def getPostForLoggedInUser(self, request):
        # since we'll get a token from the client we'll check to see what user has that auth token
        user = RareUser.objects.get(user=request.auth.user)
        # then we filter posts that have that user's id
        posts = Post.objects.filter(user=user)
        # many=True means we're inputing a list which by default is false
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST requests

        Returns:
            Response -- JSON serialized post
        """
        user = RareUser.objects.get(user=request.auth.user)

        request.data['publication_date'] = datetime.now()
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
    
    
    @action(methods=['put'], detail=True)
    def updatePostTags(self, request, pk):
        """Handles updating tags on a single post"""
        
        post = Post.objects.get(pk=pk)
        serializer = CreatePostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Post tags updated'}, status=status.HTTP_204_NO_CONTENT)

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
        fields = ('id', 'user','category','title','publication_date','image','content','approved','tags', 'comments', 'is_user')
        depth =  1

class CreatePostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ('id', 'category','title','publication_date','image_url','content','approved')
    