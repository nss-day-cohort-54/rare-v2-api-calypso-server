from django.db import models


class Post(models.Model):
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateTimeField()
    image_url = models.CharField(max_length=200)
    content = models.TextField()
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag", related_name="posts")

    @property
    def comments(self):
        return self.__comments
    @comments.setter
    def comments(self, value):
        self.__comments = value