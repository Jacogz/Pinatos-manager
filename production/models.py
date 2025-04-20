from django.db import models
from core.models import Person
from design.models import Design, Process

# Create your models here.
class Batch(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE, blank=False)
    initial_quantity = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=20, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_processes(self):
        design_processes= self.design.processes.all()
        processes = design_processes.order_by("hierarchy")
        return processes
            
        

class Workshop(models.Model):
    responsible = models.ForeignKey(Person, on_delete=models.PROTECT, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class ProcessAssignment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, blank=False)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, blank=False)
    workshop = models.ForeignKey(Workshop, on_delete=models.PROTECT, blank=False)
    status = models.CharField(max_length=20, blank=False, null=False, default='active')
    assignment_date = models.DateTimeField(blank=False, null=False)
    expected_delivery = models.DateTimeField(blank=False, null=False)
    delivery_date = models.DateTimeField(null=True)
    delivered_units = models.IntegerField(null=True)
    observation = models.TextField(null=True)