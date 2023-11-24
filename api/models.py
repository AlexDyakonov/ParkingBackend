from django.db import models


# Create your models here.

class Mock(models.Model):
    text = models.TextField(null=False, max_length=50)

    def __str__(self):
        return self.text
