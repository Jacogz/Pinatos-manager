from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import workshopCreationForm, workshopUpdateForm, batchCreationForm
from .services import productionService

ps = productionService()

def index(request):
    return render(request, 'production/productionIndex.html')

# Workshop functionalities
def workshops(request): #FR-7: CRUD workshops
    workshops = ps.get_workshops()
    return render(request, 'production/workshops.html', {'workshops': workshops})

def workshop(request, workshop_id): #FR-7: CRUD workshops
    workshop = ps.get_workshop(workshop_id)
    assignments = ps.get_assignments(workshop_id=workshop.id)
    return render(request, 'production/workshop.html', {'workshop': workshop, 'assignments': assignments})

def create_workshop(request): #FR-7: CRUD workshops
    if request.method == 'POST':
        form = workshopCreationForm(request.POST or None)
        if form.is_valid():
            new_workshop = ps.create_workshop(form)
            return redirect(f'/production/workshops/{new_workshop.id}')
    else:
        form = workshopCreationForm()
    return render(request, 'production/workshopCreationForm.html', {'form': form})

def update_workshop(request, workshop_id): #FR-7: CRUD workshops
    workshop = ps.get_workshop(workshop_id)
    if request.method == 'POST':
        form = workshopUpdateForm(request.POST or None, instance=workshop)
        if form.is_valid():
            workshop = form.save(commit=False)
            workshop.save()
            return redirect(f'/production/workshops/{workshop.id}')
    else:
        form = workshopUpdateForm(instance=workshop)
    return render(request, 'production/workshopUpdateForm.html', {'form': form})

# Batch functionalities
def batches(request): #FR-5: CRUD batches and assignment
    batches = ps.get_batches()
    return render(request, 'production/batches.html', {'batches': batches})

def batch(request, batch_id): #FR-5: CRUD batches and assignment
    batch = ps.get_batch(batch_id)
    design = batch.design
    processes = batch.get_processes()
    assignments = ps.get_assignments(batch_id=batch)
    return render(request, 'production/batch.html', {'batch': batch, 'design': design, 'processes': processes, 'assignments': assignments})

def create_batch(request): #FR-5: CRUD batches and assignment
    if request.method == 'POST':
        form = batchCreationForm(request.POST or None)
        if form.is_valid():
            new_batch = ps.create_batch(form)
            return redirect(f'/production/batches/{new_batch.id}')
    else:
        form = batchCreationForm()
    return render(request, 'production/batchCreationForm.html', {'form': form})

#Assignment functionalities

def assign_batch(request):
    if request.method == 'POST':
        form = request.POST
        batch_id = form.__getitem__('batch_id')
        ps.assign_batch(form)
    return redirect(f'/production/batches/{batch_id}')