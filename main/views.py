from django.shortcuts import render, get_object_or_404
from .models import Location
from administrator.models import Response, Incidence
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required()
def home(request):
    incedences = Response.objects.filter(responders=request.user)
    context = {
        'incedences': incedences
    }
    return render(request, 'home.html', context)


@login_required()
def usr_incident_details(request, pk):
    incident = get_object_or_404(Incidence, pk=pk)
    context = {'incident': incident}
    return render(request, 'usr_incedence_details.html', context)


@login_required()
def all_incedences(request):
    incidents = Incidence.objects.filter(status__in=['pending', 'Pending'])

    context = {
        'incidents': incidents,
    }

    return render(request, 'all_incedences.html', context)