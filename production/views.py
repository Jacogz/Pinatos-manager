from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Workshop, Batch, ProcessAssignment
from .forms import workshopCreationForm, workshopUpdateForm, batchCreationForm

def index(request):
    return render(request, 'production/productionIndex.html')

# Workshop functionalities
def workshops(request): #FR-7: CRUD workshops
    searchTerm = request.GET.get('searchWorkshop')
    if searchTerm:
        workshops = Workshop.objects.filter(name__contains=searchTerm)
    else:
        workshops = Workshop.objects.all()
    return render(request, 'production/workshops.html', {'searchTerm': searchTerm, 'workshops': workshops})

def workshop(request, workshop_id): #FR-7: CRUD workshops
    workshop = Workshop.objects.get(id=workshop_id)
    assignments = ProcessAssignment.objects.filter(workshop_id=workshop_id)
    return render(request, 'production/workshop.html', {'workshop': workshop, 'assignments': assignments})

def create_workshop(request): #FR-7: CRUD workshops
    if request.method == 'POST':
        form = workshopCreationForm(request.POST or None)
        if form.is_valid():
            new_workshop = form.save(commit=False)
            new_workshop.save()
            return redirect(f'/production/workshops/{new_workshop.id}')
    else:
        form = workshopCreationForm()
    return render(request, 'production/workshopCreationForm.html', {'form': form})

def update_workshop(request, workshop_id): #FR-7: CRUD workshops
    workshop = Workshop.objects.get(id=workshop_id)
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
    batches = Batch.objects.all()
    return render(request, 'production/batches.html', {'batches': batches})

def batch(request, batch_id): #FR-5: CRUD batches and assignment
    batch = Batch.objects.get(id=batch_id)
    design = batch.design
    processes = design.processes.all()
    return render(request, 'production/batch.html', {'batch': batch, 'design': design, 'processes': processes})

def create_batch(request): #FR-5: CRUD batches and assignment
    if request.method == 'POST':
        form = batchCreationForm(request.POST or None)
        if form.is_valid():
            new_batch = form.save(commit=False)
            new_batch.save()
            return redirect(f'/production/batches/{new_batch.id}')
    else:
        form = batchCreationForm()
    return render(request, 'production/batchCreationForm.html', {'form': form})