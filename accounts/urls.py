from django.urls import path
from . import views


# create urls 
urlpatterns = [
    path('login/', views.signin, name='login'),
    path('register_hospital', views.register_hospital, name='register_hospital'),
]