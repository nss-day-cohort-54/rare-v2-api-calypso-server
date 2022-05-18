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

    