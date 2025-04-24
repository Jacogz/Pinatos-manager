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
            result = ProcessResult(success=True, objects={'workshop': workshop})
            
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
    def get_batch_by_id(batch_id):
        # FR-21: Batch Status Visualization
        try:
            batch = Batch.objects.get(id=batch_id)
            assignments = ProcessAssignment.objects.filter(batch=batch)
            all_processes = batch.get_processes()
            processes = []
            for process in all_processes:
                assignment = assignments.filter(process=process).first()
                processes.append({
                    'process': process,
                    'assignment': assignment,
                    'is_assigned': assignment is not None
                })
            workshops = Workshop.objects.all()
            result = ProcessResult(success=True, objects={'batch': batch, 'processes': processes, 'workshops': workshops})
            
        except Batch.DoesNotExist:
            result = ProcessResult(success=False, errors="Lote no encontrado id:{batch_id}")
            
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
    def assignment_mark_reviewed(assignment_id, form_data):
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
            if not ProcessAssignment.objects.filter(batch=assignment.batch, status__in=['active', 'delivered']).exists():
                assignment.batch.status = 'completed'
                assignment.batch.save()
            
        return ProcessResult(success=True, objects={'assignment': assignment})
    
    @staticmethod
    def assign_batch(form_data, batch_id, process_id):
        #FR-5: Batch assignment
        try:
            form = ProcessAssignmentForm(form_data)
            print("DEBUG: assign_batch form data:", form.is_valid())
            if not form.is_valid():
                return ProcessResult(success=False, errors=form.errors)
            batch = Batch.objects.get(id=batch_id)
            process = batch.get_processes().get(id=process_id)
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
            
            return ProcessResult(success=True, objects={'assignment': new_assignment})
        
        except Exception as e:
            return ProcessResult(success=False, errors={'errors': str(e)})
        