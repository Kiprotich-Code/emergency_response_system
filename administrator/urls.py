from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_user/', views.user_create, name='add_user'),
    path('user_list/', views.user_list, name='user_list'),
    path('<int:pk>', views.user_detail, name='user_detail'),
    path('<int:pk>/edit/', views.user_update, name='user_update'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),

    # extras - user management home 
    path('hospital_users/', views.hospital_users, name='hospital_users'),
    path('responder_users/', views.responder_users, name='responder_users'),
    path('vehicle_users/', views.vehicle_users, name='vehicle_users'),

    # calls 
    path('record_call/', views.record_call, name='record_call'),
    path('calls/', views.calls, name='calls'),
    path('calls/<int:pk>', views.call_details, name='call_details'),
    path('calls/<int:pk>/edit/', views.call_update, name='call_update'),

    
    # Incidences 
    path('incidents/', views.incidents, name='incidents'),
    path('add_incident/', views.add_incident, name='add_incident'),
    path('incidents/<int:pk>/edit/', views.incident_update, name='incident_update'),
    path('incidents/<int:pk>', views.incident_details, name='incident_details'),
    path('incidents/<int:pk>/delete/', views.incident_delete, name='incident_delete'),

    # Assign Incidents
    path('pending_incidents/', views.pending_incidents, name='pending_incidents'),
    path('nearby_responders/<int:pk>', views.nearby_responders, name='nearby_responders'),
    path('incidents/<int:incidence_pk>/assign/<int:responder_pk>/', views.assign_incidence, name='assign_incedence'),

    # Assign Incidents to all responders 
    path('incidents/<int:incidence_pk>/assign_all/', views.assign_all_nearby_responders, name='assign_all_nearby_responders'),
]