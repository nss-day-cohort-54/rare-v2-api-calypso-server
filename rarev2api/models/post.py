from django.db import models


class Post(models.Model):
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateTimeField()
    image_url = models.TextField()
    content = models.TextField()
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag", related_name="posts")

    @property
    def comments(self):
        return self.__comments
    @comments.setter
    def comments(self, value):
        self.__comments = value
        
    @property
    def is_user(self):
        return self.__is_user
    @is_user.setter
    def is_user(self, value):
        self.__is_user = value
        
    @property
    def user_subscribed(self):
        return self.__is_user
    @user_subscribed.setter
    def user_subscibed(self, value):
        self.__is_user = value