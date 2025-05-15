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
            designs = Design.objects.filter(name__contains=search_term)
        else:
            designs = Design.objects.all()
        
        collections_dict = {}
        for design in designs:
            collection = design.collection
            if collection not in collections_dict:
                collections_dict[collection] = []
            collections_dict[collection].append(design)
        
        return collections_dict
        
    @staticmethod
    def get_all_collections(search_term=None):
        # FR-3: CRUD designs and collections (Updated to use service)
        if search_term:
            return Collection.objects.filter(name__contains=search_term)
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
    
    @staticmethod
    def delete_collection(collection_id):
        # FR-3: CRUD designs and collections (Updated to use service)
        try:
            collection = Collection.objects.get(id=collection_id)
            collection.delete()
            return ProcessResult(success=True, errors=None)
        
        except Exception as e:
            return ProcessResult(success=False, errors=str(e))
    
    @staticmethod
    def create_design(form_data, form_files):
        # FR-3: CRUD designs and collections (Updated to use service)
        form = designForm(form_data, form_files)
        
        if not form.is_valid():
            result = ProcessResult(success=False, errors=form.errors)
            return result
        
        try:
            design = form.save()
            return ProcessResult(success=True, errors=None, objects={'design': design})
        
        except Exception as e:
            return ProcessResult(success=False, errors=str(e))
    
    @staticmethod
    def update_design(design, form_data, form_files):
        # FR-3: CRUD designs and collections (Updated to use service)
        form = designUpdateForm(form_data, form_files, instance=design)
        
        if not form.is_valid():
            result = ProcessResult(success=False, errors=form.errors)
            return result
        
        try:
            design = form.save()
            return ProcessResult(success=True, errors=None, objects={'design': design})
        
        except Exception as e:
            return ProcessResult(success=False, errors=str(e))
    
    @staticmethod
    def delete_design(design_id):
        # FR-3: CRUD designs and collections (Updated to use service)
        try:
            design = Design.objects.get(id=design_id)
            design.delete()
            return ProcessResult(success=True, errors=None)
        
        except Exception as e:
            return ProcessResult(success=False, errors=str(e))