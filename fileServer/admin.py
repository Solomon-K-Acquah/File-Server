from django.contrib import admin

from fileServer.models import Category, Download, EmailLog, File, User

# show file model headings in admin panel 
class FileServerAdmin(admin.ModelAdmin):
    list_display = ('title', 'download_count', 'email_count', 'category', 'upload_date')
    list_filter = ('title', 'category', 'upload_date')
    search_fields = ('title', 'description')
    search_help_text = 'Write in your query and hit the search button'
    readonly_fields = ('download_count', 'email_count')
    ordering = ('-upload_date',)


# Model Registration
admin.site.register(User)
admin.site.register(File, FileServerAdmin)
admin.site.register(Category)
admin.site.register(Download)
admin.site.register(EmailLog)