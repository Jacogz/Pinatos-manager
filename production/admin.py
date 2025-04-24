from django.contrib import admin
from .models import Workshop, Batch, ProcessAssignment

# Register your models here.
admin.site.register(Workshop)
admin.site.register(Batch)
admin.site.register(ProcessAssignment)
