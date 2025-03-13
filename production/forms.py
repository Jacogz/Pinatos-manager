from django import forms
from .models import Workshop, Batch, ProcessAssignment

class workshopCreationForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['responsible', 'name', 'address', 'email', 'phone_number']

class workshopUpdateForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['responsible', 'name', 'address', 'email', 'phone_number']
    
    def save(self, commit=True):
        workshop = self.instance
        workshop.responsible = self.cleaned_data['responsible']
        workshop.name = self.cleaned_data['name']
        workshop.address = self.cleaned_data['address']
        workshop.email = self.cleaned_data['email']
        workshop.phone_number = self.cleaned_data['phone_number']
        if commit:
            workshop.save()
        return workshop

class batchCreationForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['design', 'initial_quantity', 'status']


    