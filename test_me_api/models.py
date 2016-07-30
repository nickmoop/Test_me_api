from django.db import models

class Text(models.Model):
    body = models.CharField(max_length = 1000)
