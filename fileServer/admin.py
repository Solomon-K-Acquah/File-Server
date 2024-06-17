from django.contrib import admin

from fileServer.models import Category, Download, EmailLog, File, User

# Model Registration
admin.site.register(User)
admin.site.register(File)
admin.site.register(Category)
admin.site.register(Download)
admin.site.register(EmailLog)