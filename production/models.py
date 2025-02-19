from django.db import models

# Create your models here.
class Batch(models.Model):
    reference = models.ForeignKey('Design', on_delete=models.CASCADE)
    programmed_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Process(models.Model):
    description = models.TextField()
    
    def __str__(self):
        return self.description

class Workshop(models.Model):
    responsible = models.ForeignKey('Person', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stage(models.Model):
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE)
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    workshop = models.ForeignKey('Workshop', on_delete=models.CASCADE)
    active = models.BooleanField()
    start_date = models.DateTimeField()
    expected_delivery_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name