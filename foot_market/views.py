from django.shortcuts import render

# Create your views here.
ERROR_500_TEMPLATE_NAME = '500.html'

def landing(request, *args, **kwargs):
    print(request.method)
    return render(request, 'base.html', {})

def home(request, *args, **kwargs):
    print(request.method)
    return render(request, 'home.html', {})

def donations(request, *args, **kwargs):
    print(request.method)
    return render(request, 'donations.html', {})