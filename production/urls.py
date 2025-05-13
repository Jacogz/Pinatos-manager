from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    #Production endpoints
    path('', views.index, name='productionIndex'),
    
    #Workshop endpoints
    path('workshops/', views.workshops, name='workshops'),
    path('workshops/<int:workshop_id>', views.workshop, name='workshop'),
    path('workshops/create', views.create_workshop, name='workshop_creation'),
    path('workshops/update/<int:workshop_id>', views.update_workshop, name='workshop_update'),
    
    #Batch endpoints
    path('batches/', views.batches, name='batches'),
    path('batches/<int:batch_id>', views.batch, name='batch'),
    path('batches/create', views.create_batch, name='batch_creation'),
    
    #Assignment endpoints
    path('batches/<int:batch_id>/assign/<int:process_id>/', views.assign_batch, name='assign_batch'),
    path('assignments/recieved/<int:assignment_id>/', views.assignment_mark_recieved, name='assignment_mark_recieved'),
    path('assignments/revised/<int:assignment_id>/', views.assignment_mark_revised, name='assignment_mark_revised'),
]