from django.db import models

# Create your models here.
class AIResponseModel(models.Model):
    image = models.ImageField()
    Pneumonia = models.BooleanField()

    def __str__(self):
        return self.Pneumonia