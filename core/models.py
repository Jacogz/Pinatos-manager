from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    document = models.PositiveBigIntegerField(max_length=15, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name