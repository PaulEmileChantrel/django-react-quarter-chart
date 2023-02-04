from django.db import models

# Create your models here.
class Compagnies(models.Model):
    name = models.CharField(max_length=100,unique=True)
    ticker = models.CharField(max_length=6)
    data_was_downloaded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image_link = models.CharField(max_length=250)
    market_cap = models.FloatField(default=0)