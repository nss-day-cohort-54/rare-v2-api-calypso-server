from django.db import models

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    content = models.CharField(max_length=199)
    created_on = models.DateTimeField()
    
    
    @property
    def is_user(self):
        return self.__is_user
    @is_user.setter
    def is_user(self, value):
        self.__is_user = value