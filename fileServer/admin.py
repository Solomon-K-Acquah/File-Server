from django.contrib import admin

from fileServer.models import Category, Download, File

# Model Registration
admin.site.register(File)
admin.site.register(Category)
admin.site.register(Download)