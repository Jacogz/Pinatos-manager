from django.db import models
from core.models import Person
from design.models import Design, Process

# Create your models here.
class Batch(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE, blank=False)
    initial_quantity = models.IntegerField(null=False, blank=False)
    final_quantity = models.IntegerField(null=True)
    status = models.CharField(max_length=20, blank=True, null=False, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_processes(self):
        design_processes= self.design.processes.all()
        all_processes = design_processes.order_by("hierarchy")
        assignments = ProcessAssignment.objects.filter(batch=self)
        processes = []
        for process in all_processes:
            assignment = assignments.filter(process=process).first()
            processes.append({
                'process': process,
                'assignment': assignment,
                'is_assigned': assignment is not None
            })
        return processes
    
    def is_completed(self):
        processes = self.get_processes()
        for process in processes:
            if not process['is_assigned'] or process['assignment'].status in ['active', 'unrevised']:
                return False
        return True
    
    def get_active_assignment(self):
        assignments = ProcessAssignment.objects.filter(batch=self)
        for assignment in assignments:
            if assignment.status == 'active':
                return assignment.process.description
        return None
        
    
    def is_active(self):
        return self.status == 'active'
    def is_pending(self):
        return self.status == 'pending'
    
            
        

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
    
    class Meta:
        get_latest_by = 'delivery_date'