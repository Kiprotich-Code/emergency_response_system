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
    return render(request, 'user_form.html', {'form': form})

# Read
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

# Update
def user_update(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=pk)
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

# Delete
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})
