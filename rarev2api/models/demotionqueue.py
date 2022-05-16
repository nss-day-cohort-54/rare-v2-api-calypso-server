from django.db import models

class DemotionQueue(models.Model):
    action = models.CharField(max_length=50)
    admin = models.ForeignKey("RareUsers", on_delete=models.CASCADE)
    approver_one = models.ForeignKey("RareUsers", on_delete=models.CASCADE)
    