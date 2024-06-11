import os
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from fileServer.models import Category, File
from django.db.models import Q

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
    
    # fetch all categories
    categories = Category.objects.all()
    
    context = {'files' : files, 'categories' : categories}
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
    

# show file based on categories
def show_file_by_category(request, slug):
    
    category = get_object_or_404(Category, slug = slug)
    files = File.objects.filter(category_id = category).order_by('-id')
    
    categories = Category.objects.all()
    
    context = {'files' : files, 'categories' : categories}
    return render(request, 'fileServer/all_files.html', context)


# function for search functionality
def search_file(request):
    # intializing search query to an empty string at the initial stage
    search_query = ''
    
    # assign the value of the search input field to the search_query
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        
    # get the files according to the search_query
    files = File.objects.filter(Q(title__icontains = search_query) | 
                                Q(description__icontains = search_query) | 
                                Q(slug__icontains = search_query))
    
    categories = Category.objects.all()
    
    context = {'files' : files, 'categories' : categories, 'search_query' : search_query}
    return render(request, 'fileServer/all_files.html', context)
    