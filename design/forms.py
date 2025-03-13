from django import forms
from .models import Collection, Design

class collectionCreationForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']
        
class collectionUpdateForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']
    
    def save(self, commit=True):
        collection = self.instance
        collection.name = self.cleaned_data['name']
        collection.description = self.cleaned_data['description']
        if commit:
            collection.save()
        return collection

class designCreationForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['collection', 'title', 'description', 'image', 'technical_sheet']
        
class designUpdateForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['collection', 'title', 'description', 'image', 'technical_sheet']

    def save(self, commit=True):
        design = self.instance
        design.collection = self.cleaned_data['collection']
        design.title = self.cleaned_data['title']
        design.description = self.cleaned_data['description']
        if self.cleaned_data['image']:
            design.image = self.cleaned_data['image']
        if self.cleaned_data['technical_sheet']:
            design.technical_sheet = self.cleaned_data['technical_sheet']
            
        if commit:
            design.save()
        return design