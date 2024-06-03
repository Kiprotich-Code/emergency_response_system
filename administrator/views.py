from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

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
