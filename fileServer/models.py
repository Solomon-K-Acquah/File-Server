import os
from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create custom user manager model
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, username, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, first_name, last_name, username, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, username, **extra_fields)
    
    def create_superuser(self, email, password, first_name, last_name, username, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, username, **extra_fields)

# Create custom user model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    
    last_login = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f'{self.username}'
    
    

# model class for category-------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200 ,unique=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
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

# Helper function to delete a file from the filesystem.
def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)
    
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
            
        # Override the save method to handle file and image updates.
        try:
            old_instance = File.objects.get(pk=self.pk)
        except File.DoesNotExist:
            old_instance = None
            
        super().save(*args, **kwargs)
        
        if old_instance:
            if old_instance.file and old_instance.file != self.file:
                delete_file(old_instance.file.path)
            if old_instance.image and old_instance.image != self.image:
                delete_file(old_instance.image.path)
        
        return super(File, self).save(*args,**kwargs)
    
    # Override the delete method to handle file and image deletions.
    def delete(self, *args, **kwargs):
        if self.file:
            delete_file(self.file.path)
        if self.image:
            delete_file(self.image.path)
        super().delete(*args, **kwargs)
        
    
#Signal to delete files and images after a model instance is deleted.
@receiver(post_delete, sender=File)
def delete_files_on_model_delete(sender, instance, **kwargs):
    if instance.file:
        delete_file(instance.file.path)
    if instance.image:
        delete_file(instance.image.path)


    
    # def save(self, *args, **kwargs):
    # try:
    #     old_instance = YourModel.objects.get(pk=self.pk)
    # except YourModel.DoesNotExist:
    #     old_instance = None

    # super().save(*args, **kwargs)

# model class for Download-------------------------------------------
class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    download_timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} downloaded "{self.file.title}"'

# model class for Email Log-------------------------------------------
class EmailLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    recipient_email = models.EmailField(max_length=200)
    send_timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} downloaded "{self.file.title}" to "{self.recipient_email}"'
    