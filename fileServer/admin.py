from urllib.parse import urlencode
from django.contrib import admin
from fileServer.models import Category, Download, EmailLog, File, User


# show file model headings in admin panel 
class FileServerAdminFile(admin.ModelAdmin):
    list_display = ('title', 'download_count', 'email_count', 'category', 'upload_date')
    list_filter = ('category', 'upload_date')
    search_fields = ('title', 'description')
    search_help_text = 'Write in your query and hit the search button'
    readonly_fields = ('download_count', 'email_count')
    ordering = ('-upload_date',)
    list_per_page = 10

    
# show users model headings in admin panel 
class FileServerUsers(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_superuser')
    list_filter = ('date_joined', 'is_active')
    search_fields = ('username', 'email')
    search_help_text = 'Write in your query and hit the search button'
    ordering = ('-username',)
    list_per_page = 10

    
# show categories model headings in admin panel 
class FileServerCategories(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')
    search_help_text = 'Write in your query and hit the search button'
    ordering = ('-name',)
    list_per_page = 10
    
    
# show downloads model headings in admin panel 
class FileServerDownloads(admin.ModelAdmin):
    list_display = ('user', 'file', 'download_timestamp')
    list_filter = ('download_timestamp', 'file', 'download_timestamp')
    ordering = ('-download_timestamp',)
    list_per_page = 10
    readonly_fields = ('user', 'file', 'download_timestamp')
    
    
# show categories model headings in admin panel 
class FileServerEmailLogs(admin.ModelAdmin):
    list_display = ('user', 'file', 'recipient_email', 'send_timestamp')
    list_filter = ('send_timestamp',)
    ordering = ('-user',)
    list_per_page = 10
    readonly_fields = ('user', 'file', 'recipient_email', 'send_timestamp')
    


# Model Registration
admin.site.register(User, FileServerUsers)
admin.site.register(File, FileServerAdminFile)
admin.site.register(Category, FileServerCategories)
admin.site.register(Download, FileServerDownloads)
admin.site.register(EmailLog, FileServerEmailLogs)