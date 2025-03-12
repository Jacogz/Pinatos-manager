from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Collection, Design
#from .forms import collectionCreationForm, collectionUpdateForm, designCreationForm, designUpdateForm

# Create your views here.
def index(request):
    return render(request, 'design/designIndex.html')

#Collection functionalities
def collections(request):
    searchTerm = request.GET.get('searchCollection')
    if searchTerm:
        collections = Collection.objects.filter(name__contains=searchTerm)
    else:
        collections = Collection.objects.all()
    return render(request, 'design/collections.html', {'searchTerm':searchTerm, 'collections': collections})

def collection(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    designs = Design.objects.filter(collection=collection)
    return render(request, 'design/collection.html', {'collection': collection, 'designs': designs})

def create_collection(request):
    if request.method == 'POST':
        form = collectionCreationForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            new_collection = Collection.objects.create(name=data['name'], description=data['description'])
            new_collection.save()
            return redirect(f'/design/collections/{new_collection.id}')
    else:
        form = collectionCreationForm()
    return render(request, 'design/collectionCreationForm.html', {'form': form})

def update_collection(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    if request.method == 'POST':
        form = collectionUpdateForm(request.POST or None, instance=collection)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            collection = obj
            return redirect(f'/design/collections/{collection.id}')
    else:
        form = collectionUpdateForm(instance=collection)
    return render(request, 'design/collectionUpdateForm.html', {'form': form})

def delete_collection(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    collection.delete()
    HttpResponse("Collection deleted successfully")
    return redirect('/design/collections')


#Design functionalities
def designs(request):
    searchTerm = request.GET.get('searchDesign')
    if searchTerm:
        designs = Design.objects.filter(title__contains=searchTerm)
    else:
        designs = Design.objects.all()
    return render(request, 'design/designs.html', {'designs': designs})

def design(request, design_reference):
    design = Design.objects.get(reference=design_reference)
    return render(request, 'design/design.html', {'design': design})

def create_design(request):
    if request.method == 'POST':
        form = designCreationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            new_design = Design.objects.create(collection=data['collection'], title=data['title'], description=data['description'], image=data['image'])
            new_design.save()
            return redirect(f'/design/designs/{new_design.reference}')
    else:
        form = designCreationForm()
    return render(request, 'design/designCreationForm.html', {'form': form})

def update_design(request, design_reference):
    design = Design.objects.get(reference=design_reference)
    if request.method == 'POST':
        form = designUpdateForm(request.POST, request.FILES, instance=design)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            design = obj
            return redirect(f'/design/designs/{design.reference}')
    else:
        form = designUpdateForm(instance=design)
    return render(request, 'design/designUpdateForm.html', {'form': form})

def delete_design(request, design_reference):
    design = Design.objects.get(reference=design_reference)
    design.delete()
    HttpResponse("Design deleted successfully")
    return redirect('/design/designs')