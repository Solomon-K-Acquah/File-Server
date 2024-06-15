from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from django.contrib.auth.models import User

# model class for category-------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200 ,unique=True)
    
    # set model object name to it title
    def __str__(self):
        return self.name
    
    # generate default slug for the file when save newly
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args,**kwargs)


# model class for file-------------------------------------------
# file max size validator
def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB limit
    if value.size > limit:
        raise ValidationError(f"Max file size is 5MB")
    
class File(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    file = models.FileField(null=True, blank=True, upload_to='files/', validators=[validate_file_size])
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    upload_date = models.DateTimeField(auto_now=True)
    download_count = models.PositiveIntegerField(default=0)
    email_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    # set model object name to it title
    def __str__(self):
        return self.title
    
    # generate default slug for the file when save newly
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        return super(File, self).save(*args,**kwargs)

# model class for Download-------------------------------------------
class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    download_timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} downloaded {self.file.title}'