from django import forms
from .models import Collection, Design

class collectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control collection-form-input', 'placeholder': 'Nombre de la colección'}),
            'description': forms.TextInput(attrs={'class': 'form-control collection-form-input', 'placeholder': 'De qué se trata esta faceta de ZIGZAG?'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        errors = []
        if Collection.objects.filter(name=name).exists():
            errors.append(forms.ValidationError('Ya existe una colección con este nombre.', code='invalid'))
        if errors:
            raise forms.ValidationError(errors)
    
    def translateLabels(self):
        self.fields['name'].label = 'Nombre'
        self.fields['description'].label = 'Descripción'

class collectionUpdateForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control collection-form-input', 'placeholder': 'Nombre de la colección'}),
            'description': forms.TextInput(attrs={'class': 'form-control collection-form-input', 'placeholder': 'De qué se trata esta faceta de ZIGZAG?'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        errors = []
        if errors:
            raise forms.ValidationError(errors)
        
    def translateLabels(self):
        self.fields['name'].label = 'Nombre'
        self.fields['description'].label = 'Descripción'
    
    def save(self, commit=True):
        collection = self.instance
        collection.name = self.cleaned_data['name']
        collection.description = self.cleaned_data['description']
        if commit:
            collection.save()
        return collection

class designForm(forms.ModelForm):
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