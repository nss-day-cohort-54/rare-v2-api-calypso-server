from django.views import View
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rarev2api.models import Category
from rest_framework.response import Response



class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields= ('id', 'label',)




class CategoryView(ViewSet):
    
    
    def list(self, request):
        
        categories = Category.objects.all()
        
        serializer = CategorySerializer(categories, many=True)
        
        return Response(serializer.data)