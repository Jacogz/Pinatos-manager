from django.urls import path
from . import views

urlpatterns = [
    #Index of design module
    path('', views.index, name='designIndex'),
    
    #Collections endpoints
    path('collections/', views.collections, name='collections'),
    path('collections/<int:collection_id>', views.collection, name='collection'),
    path('collections/create', views.create_collection, name='collection_creation'),
    path('collections/update/<int:collection_id>', views.update_collection, name='collection_update'),
    path('collections/delete/<int:collection_id>', views.delete_collection, name='collection_deletion'),
    
    #Designs endpoints
    path('designs/', views.designs, name='designs'),
    path('designs/<int:design_id>', views.design, name='design'),
    path('create', views.create, name='design_creation_form'),
    path('create/', views.create_design, name='design_creation_processing'),
    path('update/<int:design_id>', views.update, name='design_update_form'),
    path('update/<int:design_id>/', views.update_design, name='design_update_processing'),
    path('delete', views.delete, name='design_deletion'),
]