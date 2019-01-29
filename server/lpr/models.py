from django.db import models

class LrpModel(models.Model):
    
    time = models.CharField(max_length=255, null=True)
    plate = models.CharField(max_length=255, null=True)
    frame = models.IntegerField(null=True)
    