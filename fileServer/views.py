import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from fileServer.form import CustomSignupForm, SendEmailForm
from fileServer.models import Category, Download, EmailLog, File
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from allauth.account.views import SignupForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

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
    
    # get file total download, both direct and via email
    total_downloads = file.email_count + file.download_count
    
    context = {'file' : file, 'total_downloads' : total_downloads}
    return render(request, 'fileServer/details.html', context)


# function for downloading file to the PC
def download_file(request, slug):
    file = get_object_or_404(File, slug=slug)
    file_path = file.file.path
    
    if os.path.exists(file_path):
        
        # Increment download count by one
        file.download_count += 1
        file.save()
        
        # get the user and file records to the downloads table
        Download.objects.create(user=request.user, file=file)
        
        # refresh the database
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


# send document to email
def email_document(request, slug):
    file = get_object_or_404(File, slug=slug)
    
    # get the data and send to email
    if request.method == 'POST':
        email_form = SendEmailForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data['email']
            subject = 'Your requsted file'
            message = render_to_string('fileServer/message.html', {'file' : file})
            plain_message = strip_tags(message)
            email_message = EmailMessage(subject, plain_message, settings.EMAIL_HOST_USER, [email])
            email_message.attach_file(file.file.path)
            email_message.send()
            
            # increase email_count by 1 after sending the file
            file.email_count += 1
            file.save()
            
            # get the user and file records to the downloads table
            EmailLog.objects.create(user=request.user, file=file, recipient_email=email)
            
            return redirect('thank_you')
    else:
        email_form = SendEmailForm()
    
    context = {'email_form' : email_form, 'file' : file}
    
    return render(request, 'fileServer/email_document.html', context)


# thank you page function
@login_required
def thank_you(request):
    return render(request, 'fileServer/thank_you.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('/')
    else:
        form = CustomSignupForm()
    
    return render(request, 'account/signup.html', {'form': form})

# def signup_view(request):
#     if request.method == 'POST':
#         form = CustomSignupForm(request.POST)
#         if form.is_valid():
#             form.save(request)
#             return redirect('/')
#     else:
#         form = CustomSignupForm()
    
#     return render(request, 'account/signup.html', {'form':form})
        
# register new user function
# def register_user(request):
#     if request.method == 'POST':
#         register_form = NewUserForm(request.POST)
#         if register_form.is_valid():
#             user = register_form.save()
#             login(request, user)
#             return redirect('/')
#     else:   
#         register_form = NewUserForm()
    
#     context = {'register_form' : register_form}
#     return render(request, 'registration/registration.html', context)
    