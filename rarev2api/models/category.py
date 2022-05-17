from django.db import models


class Category(models.Model):
    label = models.CharField(max_length=50)
    
    #add custom property Admin -is the user and admin, if yes 
    #they can