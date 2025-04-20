from .models import Collection, Design
from .forms import collectionForm, collectionUpdateForm, designForm, designUpdateForm
from dataclasses import dataclass

@dataclass
class ProcessResult:
    success: bool
    errors: dict = None
    objects: dict = None

class DesignService:
    @staticmethod
    def get_all_designs(search_term=None):
        # FR-3: CRUD designs and collections (Updated to use service)
        if search_term:
            return Design.objects.filter(title_contains=search_term)
        else:
            return Design.objects.all()
        
    @staticmethod
    def get_all_collections(search_term=None):
        # FR-3: CRUD designs and collections (Updated to use service)
        if search_term:
            return Collection.objects.filter(name_contains=search_term)
        else:
            return Collection.objects.all()
        
    @staticmethod
    def get_design_by_id(design_id):
        # FR-3: CRUD designs and collections (Updated to use service)
        return Design.objects.get(id=design_id)
    
    @staticmethod
    def get_collection_by_id(collection_id):
        # FR-3: CRUD designs and collections (Updated to use service)
        collection = Collection.objects.get(id=collection_id)
        designs = Design.objects.filter(collection=collection)
        if(not collection):
            result = ProcessResult(success=False, errors="No se encontró la colección")
            return result
        return ProcessResult(success=True, objects={'collection': collection, 'designs': designs})
    
    @staticmethod
    def create_collection(form_data):
        # FR-3: CRUD designs and collections (Updated to use service)
        form = collectionForm(form_data)
        
        if not form.is_valid():
            result = ProcessResult(success=False, errors=form.errors)
            return result
        try:
            collection = form.save()
            return ProcessResult(success=True, errors=None, objects={'collection': collection})
        
        except Exception as e:
            return ProcessResult(success=False, errors=str(e))
    
    @staticmethod
    def update_collection(collection, form_data):
        # FR-3: CRUD designs and collections (Updated to use service)
        form = collectionUpdateForm(form_data, instance=collection)
        
        if not form.is_valid():
            result = ProcessResult(success=False, errors=form.errors)
            return result
        try:
            collection = form.save()
            return ProcessResult(success=True, errors=None, objects={'collection': collection})
        
        except Exception as e:
            return ProcessResult(success=False, errors=str(e))