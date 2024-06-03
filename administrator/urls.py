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
]