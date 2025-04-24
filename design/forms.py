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
        widgets = {
            'collection': forms.Select(attrs={'class': 'form-control design-form-input', 'placeholder':'Seleccione la colección'}),
            'title': forms.TextInput(attrs={'class': 'form-control design-form-input', 'placeholder':'Título del diseño'}),
            'description': forms.TextInput(attrs={'class': 'form-control design-form-input', 'placeholder':'Qué es esta pieza?'}),
            'image': forms.FileInput(attrs={'class': 'form-control design-form-input', 'placeholder':'Imagen del diseño'}),
            'technical_sheet': forms.FileInput(attrs={'class': 'form-control design-form-input', 'placeholder':'Archivo .xlsx'})
        }
    
    def translateLabels(self):
        self.fields['collection'].label = 'Colección'
        self.fields['title'].label = 'Título'
        self.fields['description'].label = 'Descripción'
        self.fields['image'].label = 'Imagen'
        self.fields['technical_sheet'].label = 'Ficha técnica'
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        image = cleaned_data.get('image')
        technical_sheet = cleaned_data.get('technical_sheet')
        errors = []
        if Design.objects.filter(title=title).exists():
            errors.append(forms.ValidationError('Ya existe un diseño con este título.', code='invalid'))
        if image and not image.name.endswith(('.png', '.jpg', '.jpeg')):
            errors.append(forms.ValidationError('El archivo de imagen debe ser PNG o JPG.', code='invalid'))
        if technical_sheet and not technical_sheet.name.endswith('.xlsx'):
            errors.append(forms.ValidationError('El archivo de la ficha técnica debe ser un archivo .xlsx.', code='invalid'))
        if errors:
            raise forms.ValidationError(errors)

class designUpdateForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['collection', 'title', 'description', 'image', 'technical_sheet']
        widgets = {
            'collection': forms.Select(attrs={'class': 'form-control design-form-input', 'placeholder':'Seleccionte la colección'}),
            'title': forms.TextInput(attrs={'class': 'form-control design-form-input', 'placeholder':'Título del diseño'}),
            'description': forms.TextInput(attrs={'class': 'form-control design-form-input', 'placeholder':'Qué es esta pieza?'}),
            'image': forms.FileInput(attrs={'class': 'form-control design-form-input', 'placeholder':'Imagen del diseño'}),
            'technical_sheet': forms.FileInput(attrs={'class': 'form-control design-form-input', 'placeholder':'Archivo .xlsx'})
        }
    
    def translateLabels(self):
        self.fields['collection'].label = 'Colección'
        self.fields['title'].label = 'Título'
        self.fields['description'].label = 'Descripción'
        self.fields['image'].label = 'Imagen'
        self.fields['technical_sheet'].label = 'Ficha técnica'
        
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        technical_sheet = cleaned_data.get('technical_sheet')
        errors = []
        if image and not image.name.endswith(('.png', '.jpg', '.jpeg')):
            errors.append(forms.ValidationError('El archivo de imagen debe ser PNG o JPG.', code='invalid'))
        if technical_sheet and not technical_sheet.name.endswith('.xlsx'):
            errors.append(forms.ValidationError('El archivo de la ficha técnica debe ser un archivo .xlsx.', code='invalid'))
        if errors:
            raise forms.ValidationError(errors)
        
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