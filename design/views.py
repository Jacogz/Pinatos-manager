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
    result = DesignService.delete_collection(collection_id)
    
    if not result.success:
        #print("DEBUG: collection deletion result:", result)
        return redirect('design:collection', collection_id=collection_id)
    
    return redirect('design:collections')
    


#Design functionalities
def designs(request): #FR-3: CRUD designs and collections
    searchTerm = request.GET.get('searchDesign')
    designs = DesignService.get_all_designs(searchTerm)
    
    context = {
        'designs': designs,
        'searchTerm': searchTerm
    }
    
    return render(request, 'design/designs.html', context)

def design(request, design_id): #FR-3: CRUD designs and collections
    design = DesignService.get_design_by_id(design_id)
    
    if not design:
        #print("DEBUG: design result: None")
        return redirect('design:designs')
    
    context = {
        'design': design
    }
    return render(request, 'design/design.html', context=context)

def create_design(request): #FR-3: CRUD designs and collections
    if request.method == 'POST':
        form_data = request.POST
        form_files = request.FILES
        print("DEBUG: Form data:", form_data)
        
        result = DesignService.create_design(form_data, form_files)
        print("DEBUG: create_design Result:", result)
        
        if result.success:
            return redirect('design:design', design_id=result.objects['design'].id)
        else:
            form = designForm(form_data)
            form.translateLabels()
            context = {
                'form': form,
                'errors': result.errors.items()
            }
            print("DEBUG: designForm errors:", context['errors'])
            return render (request, 'design/designForm.html', context)
    else:
        form = designForm()
        form.translateLabels()
        context = {
            'form': form
        }
        return render(request, 'design/designForm.html', context)

def update_design(request, design_id): #FR-3: CRUD designs and collections
    design = DesignService.get_design_by_id(design_id)
    
    if not design:
        #print("DEBUG: design result: None")
        return redirect('design:designs')
    
    if request.method == 'POST':
        form_data = request.POST
        form_files = request.FILES
        #print("DEBUG: Form data:", form_data)
        
        result = DesignService.update_design(design, form_data, form_files)
        #print("DEBUG: update_design Result:", result)
        
        if result.success:
            return redirect('design:design', design_id=result.objects['design'].id)
        else:
            form = designForm(form_data, form_files, instance=design)
            form.translateLabels()
            context = {
                'form': form,
                'errors': result.errors.items()
            }
            print("DEBUG: designForm errors:", context['errors'])
            return render (request, 'design/designUpdateForm.html', context)
    else:
        form = designForm(instance=design)
        form.translateLabels()
        context = {
            'form': form,
            'design': design
        }
        return render(request, 'design/designUpdateForm.html', context)


def delete_design(request, design_id): #FR-3: CRUD designs and collections
    result = DesignService.delete_design(design_id)
    
    if not result.success:
        #print("DEBUG: collection deletion result:", result)
        return redirect('design:design', design_id=design_id)
    
    return redirect('design:designs')