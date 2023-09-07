from django.db import models

class Image(models.Model):
    image = models.ImageField("")
    title = models.CharField(max_length=255, null=True, blank=True)
