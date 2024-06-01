from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')


def respondents_home(request):
    return render(request, 'respondents/respondents_home.html')