from django.db import models

# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=250, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name

class Process(models.Model):
    description = models.TextField(null=False, blank=False)
    hierarchy = models.IntegerField(blank=False)
    
    def __str__(self):
        return self.description

class Design(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, blank=False)
    image = models.ImageField(upload_to='designs/', blank=True, null=True)
    technical_sheet = models.FileField(upload_to='technical_sheets/', null=False, blank=False)
    processes = models.ManyToManyField(Process)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return 'Id: ' + str(self.id) + ' - ' + self.title + ' - ' + self.image.url
    