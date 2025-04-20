from .models import Workshop, Batch, ProcessAssignment
from .forms import workshopCreationForm, workshopUpdateForm, batchCreationForm
import datetime # Add to requirements.txt

batch_status = ['pending', 'active', 'completed']
assignment_status = ['unrevised', 'revised']

class productionService():
    workshops = Workshop.objects.all()
    batches = Batch.objects.all()
    assignments = ProcessAssignment.objects.all()
    
    def refresh(self, object=None):
        if object == 'workshops':
            self.workshops = Workshop.objects.all()
        elif object == 'batches':
            self.batches = Batch.objects.all()
        elif object == 'assignments':
            self.assignments = ProcessAssignment.objects.all()
        elif object == None:
            self.workshops = Workshop.objects.all()
            self.batches = Batch.objects.all()
            self.assignments = ProcessAssignment.objects.all()
    
# Workshop querying
    def get_workshops(self):
        return self.workshops
    
    def get_workshop(self, workshop_id):
        return Workshop.objects.get(id=workshop_id)
    
    def create_workshop(self, form):
        new_workshop = form.save(commit=False)
        new_workshop.save()
        self.refresh('workshops')
        return new_workshop
        

# Batch querying
    def get_batches(self):
        return self.batches
    
    def get_active_batches(self):
        return self.batches.filter(status='active')
    
    def get_completed_batches(self):
        return self.batches.filter(status='completed')
    
    def get_pending_batches(self):
        return self.batches.filter(status='pending')
    
    def get_batch(self, batch_id):
        return self.batches.get(id=batch_id)
    
    def create_batch(self, form):
        new_batch = form.save(commit=False)
        new_batch.save()
        self.refresh('batches')
        return new_batch
    
# Assignment querying
    def get_assignments(self, workshop_id=None, batch_id=None):
        if workshop_id:
            return self.assignments.filter(workshop_id=workshop_id)
        if batch_id:
            return self.assignments.filter(batch_id=batch_id)
        
        return self.assignments
    
    def get_assignment(self, assignment_id):
        return self.assignments.get(id=assignment_id)
    
    def get_active_assignments(self):
        return self.assignments.filter(status='active')
    
    def get_unrevised_assignments(self):
        return self.assignments.filter(status='unrevised')
    
    def get_revised_assignments(self):
        return self.assignments.filter(status='revised')

# Assign batch-workshop-process
    def assign_batch(self, form): # FR-5: Batch assignment
        batch = self.get_batch(form.__getitem__('batch_id'))
        workshop = self.get_workshop(form.__getitem__('workshop_id'))
        process = batch.get_processes().get(id=form.__getitem__('process_id'))
        expected_delivery = form.__getitem__('expected_delivery')
        new_assignment = ProcessAssignment(batch=batch, workshop=workshop, process=process, assignment_date=datetime.datetime.now(), expected_delivery=expected_delivery)
        new_assignment.save()
        self.refresh('assignments')
        return new_assignment
    
# Assignment return
    def assigned_batch_reception(self, assignment_id): # FR-8: Delivery registration
        assignment = self.get_assignment(id=assignment_id)
        assignment.delivery_date = datetime.datetime.now()
        assignment.status = 'unrevised'
        assignment.save()
        
# Assignment revision
    def assigned_batch_revision(self, assignment_id, delivered_units, observation): # FR-9: Batch revision
        assignment = self.get_assignment(assignment_id)
        assignment.status = 'revised'
        assignment.delivered_units = delivered_units
        assignment.observation = observation
        if assignment.expected_delivery.date() < assignment.delivery_date.date():
            assignment.observation += " | Late delivery"
        elif assignment.expected_delivery.date() < assignment.delivery_date.date():
            assignment.observation += " | Early delivery"
        assignment.save()
        self.refresh('assignments')
    
# Batch completion
    def complete_batch(self, batch_id): # FR-10: Batch completion (Pre-inventory)
        batch = self.get_batch(batch_id)
        batch.status = 'completed'
        batch.save()
        self.refresh('batches')