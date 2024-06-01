from django.shortcuts import render
from .models import Location

# Create your views here.
def index(request):
    locs = Location.objects.all()

    context = {
        'locs': locs
    }
    return render(request, 'index.html', context)


def respondents_home(request):
    return render(request, 'respondents/respondents_home.html')

def hospital_home(request):
    return render(request, 'respondents/hospital_home.html')