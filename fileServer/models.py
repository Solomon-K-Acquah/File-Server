from django.db import models
from django.utils.text import slugify

# model class for file
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
    

class File(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    file = models.FileField(null=True, blank=True, upload_to='files/')
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
