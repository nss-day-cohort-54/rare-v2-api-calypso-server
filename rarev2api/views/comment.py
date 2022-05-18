
from datetime import datetime
from xmlrpc.client import DateTime
from django.db import models
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from rarev2api.models import Comment
from rarev2api.models import RareUser


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'created_on', 'author', 'post', 'content')
        
class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'content', 'author', 'created_on')
    
    
    
class CommentView(ViewSet):
    
    
    def retrieve(self, request, pk):
        
        comment = Comment.objects.get(pk = pk)
        
        serializer = CommentSerializer(comment)
        
        return Response(serializer.data)
    
    
    def destroy(self, request, pk):
        
        comment = Comment.objects.get(pk = pk)
        comment.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
    def create(self, request):
        request.data['author'] = request.user.id
        request.data['created_on'] = datetime.now()
        serializer = CreateCommentSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(None, status= status.HTTP_201_CREATED)