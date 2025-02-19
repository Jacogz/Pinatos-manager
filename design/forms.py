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