from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Collection, Design
from .forms import collectionForm, designForm
from .services import DesignService


def index(request):
    return render(request, 'design/designIndex.html')

#Collection functionalities
def collections(request): #FR-3: CRUD designs and collections
    searchTerm = request.GET.get('searchCollection')
    collections = DesignService.get_all_collections(searchTerm)
    
    context = {
        'collections': collections,
        'searchTerm': searchTerm
    }
    return render(request, 'design/collections.html', context)

def collection(request, collection_id): #FR-3: CRUD designs and collections
    result = DesignService.get_collection_by_id(collection_id)
    if not result.success:
        #print("DEBUG: collection result:", result)
        return redirect('design:collections')
    context = result.objects
    collection_id = context['collection'].id
    return render(request, 'design/collection.html', context=context )

def create_collection(request): #FR-3: CRUD designs and collections
    if request.method == 'POST':
        form_data = request.POST
        #print("DEBUG: Form data:", form_data)
        
        result = DesignService.create_collection(form_data)
        #print("DEBUG: create_collection Result:", result)
        
        if result.success:
            return redirect('design:collection', collection_id=result.objects['collection'].id)
        else:
            form = collectionForm(form_data)
            context = {
                'form': form.translateLabels(),
                'errors': result.errors.items()
            }
            #print("DEBUG: collectionForm errors:", context['form'].errors.items())
            return render (request, 'design/collectionForm.html', context)
    else:
        form = collectionForm()
        form.translateLabels()
        context = {
            'form': form
        }
        return render(request, 'design/collectionForm.html', context)

def update_collection(request, collection_id): #FR-3: CRUD designs and collections
    result = DesignService.get_collection_by_id(collection_id)
    
    if not result.success:
        print("DEBUG: collection result:", result)
        return redirect('design:collections')
    
    if request.method == 'POST':
        form_data = request.POST
        #print("DEBUG: Form data:", form_data)
        result = DesignService.update_collection(result.objects['collection'], form_data)
        #print("DEBUG: update_collection Result:", result)
        
        if result.success:
            return redirect('design:collection', collection_id=result.objects['collection'].id)
        else:
            form = collectionForm(form_data)
            form.translateLabels()
            context = {
                'form': form,
                'errors': result.errors.items()
            }
            print("DEBUG: collectionForm errors:", context['form'].errors.items())
            return render (request, 'design/collectionUpdateForm.html', context)
    else:
        collection = result.objects['collection']
        form = collectionForm(instance=collection)
        form.translateLabels()
        context = {
            'form': form,
            'collection': collection
        }
        return render(request, 'design/collectionUpdateForm.html', context)
        
        
        

def delete_collection(request, collection_id): #FR-3: CRUD designs and collections
    return redirect('/')


#Design functionalities
def designs(request): #FR-3: CRUD designs and collections
    return redirect('/')

def design(request, design_id): #FR-3: CRUD designs and collections
    return redirect('/')

def create_design(request): #FR-3: CRUD designs and collections
    return redirect('/')

def update_design(request, design_id): #FR-3: CRUD designs and collections
    return redirect('/')

def delete_design(request, design_id): #FR-3: CRUD designs and collections
    return redirect('/')