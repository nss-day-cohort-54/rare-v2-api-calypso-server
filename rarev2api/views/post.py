"""View module for handling requests about posts"""
from operator import itemgetter
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rarev2api.models import Post
from rarev2api.models import RareUser
from django.db.models import Q

from rarev2api.models.comment import Comment
from rarev2api.views.comment import CommentSerializer 



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
            comments = CommentSerializer(comments, many = True)
            post = Post.objects.get(pk = pk)
            serializer = PostSerializer(post)
            post.comments = comments.data

            serializer.data['comments'] = comments.data
            print(serializer.data)
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
            posts = Post.objects.get(pk=request.category.pk).order_by(f'{order_by_category}')
        if order_by_tag is not None:
            # use the order by function to sort the posts
            posts = Post.objects.get(pk=request.tag.pk).order_by(f'{order_by_tag}')
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
                
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ('id', 'user','category','title','publication_date','image_url','content','approved','tags', 'comments')
        depth =  1

class CreatePostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ('category','title','publication_date','image_url','content','approved','tags')
    