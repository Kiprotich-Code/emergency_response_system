from django.urls import path
from . import views

# urls 
urlpatterns = [
    path('', views.index, name='index'),
    path('respondents_home/', views.respondents_home, name='respondents_home'),
    path('hospital_home/', views.hospital_home, name='hospital_home'),
]