from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('files/', views.all_files, name='files'),
    path('file_details/<slug:slug>', views.file_details, name='details'),
    path('download/<slug:slug>', views.download_file, name='download'),
    path('category/<slug:slug>', views.show_file_by_category, name='show_category'),
    path('search/', views.search_file, name='search'),
]