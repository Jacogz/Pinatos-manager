from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import workshopCreationForm, workshopUpdateForm, batchCreationForm, ProcessAssignmentForm
from .services import ProductionService

def index(request):
    return render(request, 'production/index.html')

def workshops(request):
    result = ProductionService.get_all_workshops()
    if not result.success:
        #print(DEBUG: workshops result: result)
        return redirect('production:index')
    
    workshops = result.objects['workshops']
    context = {
        'workshops': workshops,
    }
    return render(request, 'production/workshops.html', context)
        
    
def workshop(request, workshop_id):
    result = ProductionService.get_workshop_by_id(workshop_id)
    
    if not result.success:
        #print(DEBUG: workshop result: result)
        return redirect('production:index')
    
    workshop = result.objects['workshop']
    context = {
        'workshop': workshop,
    }
    return render(request, 'production/workshop.html', context)

def create_workshop(request):
    print('DEBUG: create_workshop request:', request.POST)
    if request.method == 'POST':
        
        form = workshopCreationForm(request.POST)
        result = ProductionService.create_workshop(form.cleaned_data)
        
        #print('DEBUG: create_workshop result:', result)
        if result.success:
            return redirect('production:workshops')
        else:
            form = workshopCreationForm(request.POST)
            form.translateLabels()
            context = {
                'form': form,
                'errors': result.errors
            }
            return render(request, 'production/workshopCreationForm.html', context)
    else:
        form = workshopCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'production/workshopCreationForm.html', context)

def update_workshop(request, workshop_id):
    result = ProductionService.get_workshop_by_id(workshop_id)
    
    print("DEBUG: update_workshop result:", result)
    
    if not result.success:
        return redirect('production:workshops')
    
    if request.method == 'POST':
        form_data = request.POST
        result = ProductionService.update_workshop(result.objects['workshop'], form_data)
        print("DEBUG: update_workshop result:", result.objects['workshop'].phone_number)
        
        if result.success:
            return redirect('production:workshop', workshop_id= result.objects['workshop'].id)
        else:
            form = workshopUpdateForm(form_data)
            form.translateLabels()
            context = {
                'form': form,
                'errors': result.errors
            }
            return render (request, 'production/workshopUpdateForm.html', context)
    else:
        workshop = result.objects['workshop']
        form = workshopUpdateForm(instance=workshop)
        form.translateLabels()
        context = {
            'form': form,
            'workshop': workshop
        }
        return render(request, 'production/workshopUpdateForm.html', context)

def batches(request):
    return redirect('production:index')

def batch(request, batch_id):
    result = ProductionService.get_batch_by_id(batch_id)
    
    #print('DEBUG: batch result: ', result)
    if not result.success:
        return redirect('production:batches')
    
    context = {
        'batch': result.objects['batch'],
        'processes': result.objects['processes'],
        'workshops': result.objects['workshops'],
    }
    return render(request, 'production/batch.html', context)

def create_batch(request):
    return redirect('production:index')

def assign_batch(request, batch_id, process_id):
    if request.method == 'POST':
        form_data = request.POST
        
        result = ProductionService.assign_batch(form_data, batch_id=batch_id, process_id=process_id)
        print('DEBUG: assign_batch result:', result)
        if not result.success:
            return redirect('production:productionIndex')
        return redirect('production:batch', batch_id=batch_id)

def assignment_mark_recieved(request, assignment_id):
    result = ProductionService.assignment_mark_recieved(assignment_id)
    print('DEBUG: assignment_mark_recieved result:', result)
    
    if not result.success:
        return redirect('production:productionIndex')
    
    return redirect('production:batch', batch_id=result.objects['batch'].id)