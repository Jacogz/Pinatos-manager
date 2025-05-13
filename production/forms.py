from django.utils.timezone import timezone
from django import forms
from .models import Workshop, Batch, ProcessAssignment


class workshopCreationForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['responsible', 'name', 'address', 'email', 'phone_number']
        widgets = {
            'responsible': forms.Select(attrs={'class': 'form-control workshop-form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control workshop-form-input', 'placeholder': 'Nombre del Taller'}),
            'address': forms.TextInput(attrs={'class': 'form-control workshop-form-input', 'placeholder': 'Dirección del Taller'}),
            'email': forms.EmailInput(attrs={'class': 'form-control workshop-form-input', 'placeholder': 'Correo electrónico'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control workshop-form-input', 'placeholder': 'Teléfono de contacto', 'pattern': r'^\+?[\d\s\-]{10,15}$'}),
        }
    
    def translateLabels(self):
        self.fields['responsible'].label = 'Responsable'
        self.fields['name'].label = 'Nombre del Taller'
        self.fields['address'].label = 'Dirección del Taller'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['phone_number'].label = 'Teléfono de contacto'

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        if not email and not phone_number:
            raise forms.ValidationError("Ingrese al menos un medio de contacto (correo o teléfono).")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap's 'is-invalid' class automatically for error fields
        for field in self.fields:
            if self.errors.get(field):
                self.fields[field].widget.attrs.update({'class': 'form-control is-invalid'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.strip():
            raise forms.ValidationError("El nombre no puede estar vacío.")
        if Workshop.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Ya existe un taller con este nombre.")
        return name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith(('.co', '.com')):  # Basic domain check
            raise forms.ValidationError("Ingrese un correo válido (dominio .co o .com).")
        return email
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove spaces/dashes for validation
            clean_phone = ''.join(c for c in phone if c.isdigit())
            if len(clean_phone) != 10:
                raise forms.ValidationError("Número debe tener 10 dígitos (ej: 9123456780).")
        return phone  # Return original to preserve formatting
        
    

class workshopUpdateForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['responsible', 'name', 'address', 'email', 'phone_number']
        widgets = {
            'responsible': forms.Select(attrs={'class': 'form-control workshop-form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control workshop-form-input', 'placeholder': 'Nombre del Taller'}),
            'address': forms.TextInput(attrs={'class': 'form-control workshop-form-input', 'placeholder': 'Dirección del Taller'}),
            'email': forms.EmailInput(attrs={'class': 'form-control workshop-form-input', 'placeholder': 'Correo electrónico'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control workshop-form-input', 'placeholder': 'Teléfono de contacto', 'pattern': r'^\+?[\d\s\-]{10,15}$'}),
        }
    
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
    
    def translateLabels(self):
        self.fields['responsible'].label = 'Responsable'
        self.fields['name'].label = 'Nombre del Taller'
        self.fields['address'].label = 'Dirección del Taller'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['phone_number'].label = 'Teléfono de contacto'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap's 'is-invalid' class automatically for error fields
        for field in self.fields:
            if self.errors.get(field):
                self.fields[field].widget.attrs.update({'class': 'form-control is-invalid'})
                
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        if not email and not phone_number:
            raise forms.ValidationError("Ingrese al menos un medio de contacto (correo o teléfono).")
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith(('.co', '.com')):  # Basic domain check
            raise forms.ValidationError("Ingrese un correo válido (dominio .co o .com).")
        return email
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove spaces/dashes for validation
            clean_phone = ''.join(c for c in phone if c.isdigit())
            if len(clean_phone) != 10:
                raise forms.ValidationError("Número debe tener 10 dígitos (ej: 9123456780).")
        return phone  # Return original to preserve formatting


class batchCreationForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['design', 'initial_quantity', 'status']
    
    def translateLabels(self):
        self.fields['design'].label = 'Diseño'
        self.fields['initial_quantity'].label = 'Cantidad inicial'
        self.fields['status'].label = 'Estado'

class ProcessAssignmentForm(forms.ModelForm):
    class Meta:
        model = ProcessAssignment
        fields = ['workshop', 'expected_delivery']
        widgets = {
            'expected_delivery': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert to naive datetime for the browser input if needed
        if self.instance and self.instance.expected_delivery:
            self.initial['expected_delivery'] = timezone.localtime(
                self.instance.expected_delivery
            ).replace(tzinfo=None)


class assignmentRevisionForm(forms.ModelForm):
    class Meta:
        model = ProcessAssignment
        fields = ['delivered_units', 'observation']
        labels = {
            'delivered_units': 'Unidades entregadas'
        }
    def save(self, commit=True):
        process_assignment = self.instance
        process_assignment.delivered_units = self.cleaned_data['delivered_units']
        process_assignment.observation = process_assignment.observation + self.cleaned_data['observation']
        if commit:
            process_assignment.save()
        return process_assignment
        


    