from django.urls import path
from . import views

# urls 
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('home/<int:pk>', views.usr_incident_details, name='usr_incident_detail'),
    path('all_incedences/', views.all_incedences, name='all_incedences'),
    path('incidences_list/', views.incidences_list, name='incidences_list'),
    path('vehicles_list/', views.vehicles_list, name='vehicles_list'),
    path('update_location/', views.update_location, name='update_location'),
]