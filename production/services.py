import pytz
from .models import Workshop, Batch, ProcessAssignment
from .forms import workshopCreationForm, workshopUpdateForm, batchCreationForm, assignmentRevisionForm, ProcessAssignmentForm
from dataclasses import dataclass
import datetime # Add to requirements.txt
from django.utils.timezone import timezone

batch_status = ['pending', 'active', 'completed']
assignment_status = ['active', 'unrevised', 'revised']

@dataclass
class ProcessResult:
    success: bool
    errors: dict = None
    objects: dict = None

class ProductionService:
    @staticmethod
    def get_all_workshops():
        # FR-7: CRUD Workshops (Service outsourced)
        try:
            workshops = Workshop.objects.all()
            result = ProcessResult(success=True, objects={'workshops': workshops})
        except Exception as e:
            result = ProcessResult(success=False, errors={'errors': str(e)})
            
        return result
    
    @staticmethod
    def get_workshop_by_id(workshop_id):
        # FR-7: CRUD Workshops (Service outsourced)
        try:
            workshop = Workshop.objects.get(id=workshop_id)
            assignments = ProcessAssignment.objects.filter(workshop=workshop)
            
            active_assignments = assignments.filter(status='active')
            unrevised_assignments = assignments.filter(status='unrevised')
            revised_assignments = assignments.filter(status='revised')
            
            
            result = ProcessResult(success=True, objects={'workshop': workshop, 'active_assignments': active_assignments, 'unrevised_assignments': unrevised_assignments, 'revised_assignments': revised_assignments})
            
        except Workshop.DoesNotExist:
            result = ProcessResult(success=False, errors="Taller no encontrado id:{workshop_id}")
        
        except Exception as e:
            result = ProcessResult(success=False, errors={'errors': str(e)})
            
        return result
    
    @staticmethod
    def create_workshop(form_data):
        # FR-7: CRUD Workshops (Service outsourced)
        try:
            form = workshopCreationForm(form_data)
            if form.is_valid():
                workshop = form.save()
                result = ProcessResult(success=True, objects={'workshop': workshop})
            else:
                result = ProcessResult(success=False, errors=form.errors)
        except Exception as e:
            result = ProcessResult(success=False, errors={'errors': str(e)})
            
        return result

    @staticmethod
    def update_workshop(workshop, form_data):
        # FR-7: CRUD Workshops (Service outsourced)
        form = workshopUpdateForm(form_data, instance=workshop)
        
        if not form.is_valid():
            result = ProcessResult(success=False, errors=form.errors)
            return result
        
        try:
            workshop = form.save()
            return ProcessResult(success=True, errors=None, objects={'workshop': workshop})
        
        except Exception as e:
            return ProcessResult(success=False, errors=str(e))
    
    @staticmethod
    def get_all_batches():
        # FR-21: Batch Status Visualization
        try:
            batches = Batch.objects.all()
            result = ProcessResult(success=True, objects={'batches': batches})
            
        except Exception as e:
            result = ProcessResult(success=False, errors={'errors': str(e)})
            
        return result
    
    @staticmethod
    def get_active_batches():
        # FR-21: Batch Status Visualization
        try:
            active_batches = Batch.objects.filter(status__in=['active', 'pending'])
            batches = [
                {
                    'batch': batch,
                    'active_assignment': batch.get_active_assignment()
                }
                for batch in active_batches
            ]

            result = ProcessResult(success=True, objects={'batches': batches})
            
        except Exception as e:
            result = ProcessResult(success=False, errors={'errors': str(e)})
            
        return result
    
    @staticmethod
    def get_completed_batches():
        # FR-21: Batch Status Visualization
        try:
            batches = Batch.objects.filter(status='completed')
            result = ProcessResult(success=True, objects={'batches': batches})
            
        except Exception as e:
            result = ProcessResult(success=False, errors={'errors': str(e)})
            
        return result
    
    @staticmethod
    def get_batch_by_id(batch_id):
        # FR-21: Batch Status Visualization
        try:
            batch = Batch.objects.get(id=batch_id)
            processes = batch.get_processes()
            workshops = Workshop.objects.all()
            result = ProcessResult(success=True, objects={'batch': batch, 'processes': processes, 'workshops': workshops})
            
        except Batch.DoesNotExist:
            result = ProcessResult(success=False, errors="Lote no encontrado id:{batch_id}")
            
        except Exception as e:
            result = ProcessResult(success=False, errors={'errors': str(e)})
            
        return result
    
    @staticmethod
    def create_batch(form_data):
        # FR-21: Batch Status Visualization
        try:
            form = batchCreationForm(form_data)
            if form.is_valid():
                batch = form.save()
                result = ProcessResult(success=True, objects={'batch': batch})
            else:
                result = ProcessResult(success=False, errors=form.errors)
        except Exception as e:
            result = ProcessResult(success=False, errors={'errors': str(e)})
            
        return result
    
    @staticmethod
    def assignment_mark_recieved(assignment_id):
        #FR-8: Assignment status update: Recieved/Unrevised
        assignment = ProcessAssignment.objects.get(id=assignment_id)
        if not assignment:
            return ProcessResult(success=False, errors="Asignación no encontrada id:{assignment_id}")
        
        try: 
            assignment.status = 'unrevised'
            assignment.delivery_date = datetime.datetime.now(pytz.UTC)
            if assignment.delivery_date > assignment.expected_delivery:
                assignment.observation = "Entrega tardía. "
            assignment.save()
            return ProcessResult(success=True, objects={'batch': assignment.batch})
        except Exception as e:
            return ProcessResult(success=False, errors={'errors': str(e)})
    
    @staticmethod
    def assignment_mark_revised(assignment_id, form_data):
        #FR-9: Assignment status update: revised/completed
        assignment = ProcessAssignment.objects.get(id=assignment_id)
        
        if not assignment:
            return ProcessResult(success=False, errors="Asignación no encontrada id:{assignment_id}")
        
        form = assignmentRevisionForm(form_data, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.status = 'revised'
            assignment.save()
            
            # Update batch status if all processes are complete
            batch = assignment.batch
            if batch.is_completed():
                assignment.batch.status = 'completed'
                assignment.batch.final_quantity = assignment.delivered_units
                assignment.batch.save()
            
            return ProcessResult(success=True, objects={'assignment': assignment, 'batch': assignment.batch})
        else:
            return ProcessResult(success=False, errors=form.errors)
    
    @staticmethod
    def assign_batch(form_data, batch_id, process_id):
        #FR-5: Batch assignment
        try:
            form = ProcessAssignmentForm(form_data)
            #print("DEBUG: assign_batch form data:", form.is_valid())
            if not form.is_valid():
                return ProcessResult(success=False, errors=form.errors)
            batch = Batch.objects.get(id=batch_id)
            process = batch.design.processes.get(id=process_id)
            workshop = form.cleaned_data['workshop']
            expected_delivery = form_data['expected_delivery']
            
            new_assignment = ProcessAssignment(
                batch=batch,
                process=process,
                workshop=workshop,
                assignment_date=datetime.datetime.now(),
                expected_delivery=expected_delivery
            )
            new_assignment.save()
            
            if batch.status == 'pending':
                batch.status = 'active'
                batch.save()
            
            return ProcessResult(success=True, objects={'assignment': new_assignment})
        
        except Exception as e:
            return ProcessResult(success=False, errors={'errors': str(e)})
        