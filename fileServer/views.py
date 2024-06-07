from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from fileServer.models import File

# Create your views here.

# funtion to handle home page view
def home_page(request):
    
    # fetch three recent files to the home page
    files = File.objects.all().order_by('-id')[0:3]
    
    context = {'files' : files }
    return render(request, 'fileServer/index.html', context)


# funtion to handle details page view
def all_files(request):
    
    # fetch all the file objects in descending order
    files = File.objects.all().order_by('-id')
    
    context = {'files' : files}
    return render(request, 'fileServer/all_files.html', context)


# function to handle file details
def file_details(request, slug):
    
    # fetch the detail of a single file or selected file
    file = File.objects.get(slug = slug)
    
    context = {'file' : file}
    return render(request, 'fileServer/details.html', context)