from django.shortcuts import render, get_object_or_404, redirect
from .models import Location
from administrator.models import Response, Incidence
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from accounts.models import CustomUser
import json

# Create your views here.
def index(request):
    incidents_list = Incidence.objects.all().order_by('-time_of_incident')
    paginator = Paginator(incidents_list, 10)

    page_number = request.GET.get('page')  # Get the current page number from the request
    incidences = paginator.get_page(page_number)

    # vehicles 
    vehicles = CustomUser.objects.filter(user_type='vehicle').prefetch_related('location')

    context = {
        'incidences': incidences,
        'vehicles': list(vehicles)
    }
    return render(request, 'index.html', context)

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

def incidences_list(request):
    incidences = Incidence.objects.select_related('location').all()
    data = [
        {
            'id': inc.id,
            'type': inc.incidence_type,
            'status': inc.status,
            'description': inc.desc,
            'address': inc.location.address,
            'lat': inc.location.lat,
            'lon': inc.location.lon,
        }
        for inc in incidences
    ]
    return JsonResponse(data, safe=False)


def vehicles_list(request):
    vehicles = CustomUser.objects.filter(user_type='Vehicle').select_related('location').values('email', 'full_names', 'location__lat', 'location__lon')
    return JsonResponse(list(vehicles), safe=False)


@login_required
def update_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lat = data.get('lat')
        lon = data.get('lon')

        # Update the user's location
        user = request.user
        user.location.lat = lat
        user.location.lon = lon
        user.location.save()  # Save the updated location

        return JsonResponse({'status': 'success', 'message': 'Location updated successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)