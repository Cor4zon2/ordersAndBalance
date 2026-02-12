from django.db import models

# Create your models here.
class Order(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    created_at = models.DateField()

    def __str__(self):
        return self.title

