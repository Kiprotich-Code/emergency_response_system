from django.urls import path
from . import views

# urls 
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('home/<int:pk>', views.usr_incident_details, name='usr_incident_detail'),
    path('all_incedences/', views.all_incedences, name='all_incedences'),
]