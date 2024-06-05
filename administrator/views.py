from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Calls, Incidence, Response
from .forms import RecordCallForm, IncidenceForm, AssignResponseForm
from django.contrib.auth.decorators import login_required
from .harversine import find_nearby_responders, haversine

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

# Admin - User Management 
# Create
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/user_form.html', {'form': form})

# Read
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    recent_users = CustomUser.objects.all().order_by('-date_joined')[0:3]
    context = {
        'users': users,
        'recent_users': recent_users
    }
    return render(request, 'users/user_home.html', context)

def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})

# Update
def user_update(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/user_update.html', {'form': form})

# Delete
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})


# Extras - Views on Users 
def recent_users(request):
    recent_users = CustomUser.objects.all().order_by('-date_joined')[0:3]
    context = {
        'recent_users': recent_users
    }
    return render(request, 'users/recent_users', context)

def hospital_users(request):
    users = CustomUser.objects.filter(user_type__in=['Hospital', 'hospital']).order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'users/hospitals_list.html', context)

def vehicle_users(request):
    users = CustomUser.objects.filter(user_type__in=['vehicle', 'Vehicle']).order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'users/vehicles_list.html', context)

def responder_users(request):
    users = CustomUser.objects.filter(user_type__in=['Responder', 'responder']).order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'users/responders_list.html', context)


# Admin - managing calls 
# Calls - admin managing calls 
def record_call(request):
    if request.method == 'POST':
        form = RecordCallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calls')
    else:
        form = RecordCallForm()
    return render(request, 'calls/record_call.html', {'form': form})

# Read
def calls(request):
    calls = Calls.objects.all().order_by('-time_of_call')
    recent_calls = Calls.objects.all().order_by('-time_of_call')[0:3]
    context = {
        'calls': calls,
        'recent_calls': recent_calls
    }
    return render(request, 'calls/calls.html', context)


def call_details(request, pk):
    call = get_object_or_404(Calls, pk=pk)
    context = {'call': call}
    return render(request, 'calls/call_details.html', context)

# Update
def call_update(request, pk):
    call = get_object_or_404(Calls, pk=pk)
    if request.method == 'POST':
        form = RecordCallForm(request.POST, instance=call)
        if form.is_valid():
            form.save()
            return redirect('calls')
    else:
        form = RecordCallForm(instance=call)

    context = {'form': form}
    return render(request, 'calls/call_update.html', context)


# Admin Views - Manage Incidences 
# Retrieve
def incidents(request):
    incidents = Incidence.objects.all().order_by('-time_of_incident')
    recent_incidents = Incidence.objects.all().order_by('-time_of_incident')[0:3]

    context = {
        'incidents': incidents,
        'recent_incidents': recent_incidents
    }

    return render(request, 'incidents/incidents.html', context)

# Create
def add_incident(request):
    if request.method == 'POST':
        form = IncidenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('incidents')
        
    else:
        form = IncidenceForm()

    context = {
        'form': form
    }
    return render(request, 'incidents/add_incident.html', context)


# Update
def incident_update(request, pk):
    incident = get_object_or_404(Incidence, pk=pk)
    if request.method == 'POST':
        form = IncidenceForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            return redirect('incidents')
    else:
        form = IncidenceForm(instance=incident)
    return render(request, 'incidents/incident_update.html', {'form': form})

# Delete
def incident_delete(request, pk):
    incident = get_object_or_404(Incidence, pk=pk)
    if request.method == 'POST':
        incident.delete()
        return redirect('incidents')
    return render(request, 'incidents/incident_confirm_delete.html', {'incident': incident})


def incident_details(request, pk):
    incident = get_object_or_404(Incidence, pk=pk)
    context = {'incident': incident}
    return render(request, 'incidents/incident_details.html', context)


# MVP - ASSIGNING INCIDENCES TO RESPONDERS 
# list view 
def pending_incidents(request):
    pending_incidences = Incidence.objects.filter(status__in=['Pending', 'pending'])

    context = {
        'pending_incidences': pending_incidences
    }

    return render(request, 'response/pending_incidences.html', context)


def nearby_responders(request, pk):
    incidence = get_object_or_404(Incidence, pk=pk)
    location = incidence.location
    responders = find_nearby_responders(location.lat, location.lon, radius=10)

    context = {
        'incidence': incidence,
        'responders': responders
    }

    return render(request, 'response/nearby_responders.html', context)


def assign_incidence(request, incidence_pk, responder_pk):
    incidence = get_object_or_404(Incidence, pk=incidence_pk)
    responder = get_object_or_404(CustomUser, pk=responder_pk)
    
    if request.method == 'POST':
        form = AssignResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.incident = incidence
            response.save()
            response.responders.add(responder)
            response.save()
            incidence.status = 'assigned'
            incidence.save()
            return redirect('pending_incidents')
    else:
        form = AssignResponseForm()

    context = {
        'form': form,
        'incidence': incidence,
        'responder': responder,
    }
        
    return render(request, 'response/assign_incedence.html', context)
