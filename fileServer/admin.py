from django.contrib import admin

from fileServer.models import Category, File

# Model Registration
admin.site.register(File)
admin.site.register(Category)
