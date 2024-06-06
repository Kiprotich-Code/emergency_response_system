from django.shortcuts import render, redirect, get_object_or_404
from .models import Calls, Incidence, Response, CustomUser
from .forms import RecordCallForm, IncidenceForm, AssignResponseForm, CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .harversine import find_nearby_responders, haversine

# Create your views here.
def is_superuser(request):
    return is_superuser

@login_required
@user_passes_test(is_superuser)
def dashboard(request):
    return render(request, 'dashboard.html')

# ADMIN - UPDATE PROFILE 
@login_required
@user_passes_test(is_superuser)
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})


# Admin - User Management 
# Create
@login_required
@user_passes_test(is_superuser)
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
@login_required
@user_passes_test(is_superuser)
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    recent_users = CustomUser.objects.all().order_by('-date_joined')[0:3]
    context = {
        'users': users,
        'recent_users': recent_users
    }
    return render(request, 'users/user_home.html', context)

@login_required
@user_passes_test(is_superuser)
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})

# Update
@login_required
@user_passes_test(is_superuser)
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
@login_required
@user_passes_test(is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})


# Extras - Views on Users 
@login_required
@user_passes_test(is_superuser)
def recent_users(request):
    recent_users = CustomUser.objects.all().order_by('-date_joined')[0:3]
    context = {
        'recent_users': recent_users
    }
    return render(request, 'users/recent_users', context)

@login_required
@user_passes_test(is_superuser)
def hospital_users(request):
    users = CustomUser.objects.filter(user_type__in=['Hospital', 'hospital']).order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'users/hospitals_list.html', context)

@login_required
@user_passes_test(is_superuser)
def vehicle_users(request):
    users = CustomUser.objects.filter(user_type__in=['vehicle', 'Vehicle']).order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'users/vehicles_list.html', context)

@login_required
@user_passes_test(is_superuser)
def responder_users(request):
    users = CustomUser.objects.filter(user_type__in=['Responder', 'responder']).order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'users/responders_list.html', context)


# Admin - managing calls 
# Calls - admin managing calls 
@login_required
@user_passes_test(is_superuser)
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
@login_required
@user_passes_test(is_superuser)
def calls(request):
    calls = Calls.objects.all().order_by('-time_of_call')
    recent_calls = Calls.objects.all().order_by('-time_of_call')[0:3]
    context = {
        'calls': calls,
        'recent_calls': recent_calls
    }
    return render(request, 'calls/calls.html', context)


@login_required
@user_passes_test(is_superuser)
def call_details(request, pk):
    call = get_object_or_404(Calls, pk=pk)
    context = {'call': call}
    return render(request, 'calls/call_details.html', context)

# Update
@login_required
@user_passes_test(is_superuser)
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
@login_required
@user_passes_test(is_superuser)
def incidents(request):
    incidents = Incidence.objects.all().order_by('-time_of_incident')
    recent_incidents = Incidence.objects.all().order_by('-time_of_incident')[0:3]

    context = {
        'incidents': incidents,
        'recent_incidents': recent_incidents
    }

    return render(request, 'incidents/incidents.html', context)

# Create
@login_required
@user_passes_test(is_superuser)
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
@login_required
@user_passes_test(is_superuser)
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
@login_required
@user_passes_test(is_superuser)
def incident_delete(request, pk):
    incident = get_object_or_404(Incidence, pk=pk)
    if request.method == 'POST':
        incident.delete()
        return redirect('incidents')
    return render(request, 'incidents/incident_confirm_delete.html', {'incident': incident})


@login_required
@user_passes_test(is_superuser)
def incident_details(request, pk):
    incident = get_object_or_404(Incidence, pk=pk)
    context = {'incident': incident}
    return render(request, 'incidents/incident_details.html', context)


# MVP - ASSIGNING INCIDENCES TO RESPONDERS 
# list view 
@login_required
@user_passes_test(is_superuser)
def pending_incidents(request):
    pending_incidences = Incidence.objects.filter(status__in=['Pending', 'pending'])

    context = {
        'pending_incidences': pending_incidences
    }

    return render(request, 'response/pending_incidences.html', context)


@login_required
@user_passes_test(is_superuser)
def nearby_responders(request, pk):
    incidence = get_object_or_404(Incidence, pk=pk)
    location = incidence.location
    responders = find_nearby_responders(location.lat, location.lon, radius=10)

    context = {
        'incidence': incidence,
        'responders': responders
    }

    return render(request, 'response/nearby_responders.html', context)


@login_required
@user_passes_test(is_superuser)
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


@login_required
@user_passes_test(is_superuser)
def assign_all_nearby_responders(request, incidence_pk):
    incidence = get_object_or_404(Incidence, pk=incidence_pk)
    location = incidence.location
    nearby_responders = find_nearby_responders(location.lat, location.lon, radius=10)  # Adjust radius as needed
    
    if request.method == 'POST':
        response = Response.objects.create(
            incident=incidence,
            message="Assigned to all nearby responders."
        )
        for responder in nearby_responders:
            response.responders.add(responder)
        response.save()
        incidence.status = 'assigned'
        incidence.save()
        return redirect('pending_incidents')  # Adjust the redirect as necessary

    context = {
        'incidence': incidence,
        'responders': nearby_responders,
    }
    
    return render(request, 'response/assign_all_nearby_responders.html', context)