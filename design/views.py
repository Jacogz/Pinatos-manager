from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Collection, Design
from .forms import collectionCreationForm, collectionUpdateForm, designCreationForm, designUpdateForm


def index(request):
    return render(request, 'design/designIndex.html')

#Collection functionalities
def collections(request): #FR-3: CRUD designs and collections
    searchTerm = request.GET.get('searchCollection')
    if searchTerm:
        collections = Collection.objects.filter(name__contains=searchTerm)
    else:
        collections = Collection.objects.all()
    return render(request, 'design/collections.html', {'searchTerm':searchTerm, 'collections': collections})

def collection(request, collection_id): #FR-3: CRUD designs and collections
    collection = Collection.objects.get(id=collection_id)
    designs = Design.objects.filter(collection=collection)
    return render(request, 'design/collection.html', {'collection': collection, 'designs': designs})

def create_collection(request): #FR-3: CRUD designs and collections
    if request.method == 'POST':
        form = collectionCreationForm(request.POST or None)
        if form.is_valid():
            new_collection = form.save(commit=False)
            new_collection.save()
            return redirect(f'/design/collections/{new_collection.id}')
    else:
        form = collectionCreationForm()
    return render(request, 'design/collectionCreationForm.html', {'form': form})

def update_collection(request, collection_id): #FR-3: CRUD designs and collections
    collection = Collection.objects.get(id=collection_id)
    if request.method == 'POST':
        form = collectionUpdateForm(request.POST or None, instance=collection)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.save()
            return redirect(f'/design/collections/{collection.id}')
    else:
        form = collectionUpdateForm(instance=collection)
    return render(request, 'design/collectionUpdateForm.html', {'form': form})

def delete_collection(request, collection_id): #FR-3: CRUD designs and collections
    collection = Collection.objects.get(id=collection_id)
    collection.delete()
    HttpResponse("Collection deleted successfully")
    return redirect('/design/collections')


#Design functionalities
def designs(request): #FR-3: CRUD designs and collections
    searchTerm = request.GET.get('searchDesign')
    if searchTerm:
        designs = Design.objects.filter(title__contains=searchTerm)
    else:
        designs = Design.objects.all()
    return render(request, 'design/designs.html', {'designs': designs})

def design(request, design_id): #FR-3: CRUD designs and collections
    design = Design.objects.get(id=design_id)
    return render(request, 'design/design.html', {'design': design})

def create_design(request): #FR-3: CRUD designs and collections
    if request.method == 'POST':
        form = designCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_design = form.save(commit=False)
            new_design.save()
            return redirect(f'/design/designs/{new_design.id}')
    else:
        form = designCreationForm()
    return render(request, 'design/designCreationForm.html', {'form': form})

def update_design(request, design_id): #FR-3: CRUD designs and collections
    design = Design.objects.get(id=design_id)
    if request.method == 'POST':
        form = designUpdateForm(request.POST, request.FILES, instance=design)
        if form.is_valid():
            new_design = form.save(commit=False)
            new_design.save()
            return redirect(f'/design/designs/{new_design.id}')
    else:
        form = designUpdateForm(instance=design)
    return render(request, 'design/designUpdateForm.html', {'form': form})

def delete_design(request, design_id): #FR-3: CRUD designs and collections
    design = Design.objects.get(id=design_id)
    design.delete()
    HttpResponse("Design deleted successfully")
    return redirect('/design/designs')