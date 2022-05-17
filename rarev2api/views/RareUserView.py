from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rarev2api.models.rareuser import RareUser
from django.contrib.auth.models import User

class RareUserView(ViewSet):
    """Rare V2 Category View"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single RareUser
        
        Returns: 
            Response -- JSON serialized RareUser
        """
        try:
            rareUser = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(rareUser)
            return Response(serializer.data)
        except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all RareUsers
        
        Returns:
            Response -- JSON serialized list of RareUsers
        """
        rareUsers = RareUser.objects.all()
        serializer = RareUserSerializer(rareUsers, many=True)
        return Response(serializer.data)
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')

        
class RareUserSerializer(serializers.ModelSerializer):
    user= UserSerializer()
    
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'active', 'user')
        depth = 1  

