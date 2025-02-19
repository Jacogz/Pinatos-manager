from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Collection, Design
from .forms import collectionCreationForm, collectionUpdateForm

# Create your views here.
def index(request):
    return render(request, 'designIndex.html')

#Collection functionalities
def collections(request):
    searchTerm = request.GET.get('searchCollection')
    if searchTerm:
        collections = Collection.objects.filter(name__contains=searchTerm)
    else:
        collections = Collection.objects.all()
    return render(request, 'collections.html', {'searchTerm':searchTerm, 'collections': collections})

def collection(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    return render(request, 'collection.html', {'collection': collection})

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
    return render(request, 'collectionCreationForm.html', {'form': form})

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
        form = collectionUpdateForm(initial={'name': collection.name, 'description': collection.description})
    return render(request, 'collectionUpdateForm.html', {'form': form})

def delete_collection(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    collection.delete()
    HttpResponse("Collection deleted successfully")
    return redirect('/design/collections')

#Design functionalities
def designs(request):
    return HttpResponse("Designs view")

def design(request):
    return HttpResponse("Design view")

def create(request):
    return render(request, 'designCreationForm.html')

def create_design(request):
    return HttpResponse("Create design processing view")

def update(request):
    return HttpResponse("Update design view")

def update_design(request):
    return HttpResponse("Update design processing view")

def delete(request):
    return HttpResponse("Delete design view")