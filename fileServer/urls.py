from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('files/', views.all_files, name='files_page')
]