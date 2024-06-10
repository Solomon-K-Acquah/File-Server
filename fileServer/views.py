from fileinput import filename
import os
from traceback import print_tb
from urllib import response
from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from fileServer import models
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

# function for downloading file to the PC
def download_file(request, slug):
    file = get_object_or_404(File, slug=slug)
    file_path = file.file.path
    
    if os.path.exists(file_path):
        
        # Increment download count by one
        file.download_count += 1
        file.save()
        
        file.refresh_from_db()
        
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    else:
        return Http404('File not found')
        
    
    