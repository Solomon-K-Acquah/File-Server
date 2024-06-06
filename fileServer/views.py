from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.

# funtion to handle home page view
def home_page(request):
    context = {'name' : 'Solomon' }
    return render(request, 'index.html', context)


# funtion to handle details page view
def all_files(request):
    context = {}
    return render(request, 'all_files.html', context)