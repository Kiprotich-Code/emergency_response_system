from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, HospitalRegisterForm

# Create your views here.
def register_hospital(request):
    if request.method == 'POST':
        form = HospitalRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'hospital'
            user.save()
            return redirect('login')
        
    else:
        form = HospitalRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'register_hospital.html', context)

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            
            # redirect users based on roles
            if user.user_type == 'hospital':
                return redirect('hospital_home')
            
            elif user.is_staff:
                return redirect('dashboard')
            
        else:
            return redirect('login') 

    else:
        form = LoginForm()
    context = {
        'form': form
    }
        
    return render(request, 'login.html', context)


def signout(request):
    logout(request)
    return redirect('index')