from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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
    username = models.CharField(max_length=200)
    
    last_login = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    

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
        return f'{self.user.username} downloaded "{self.file.title}"'

# model class for Email Log-------------------------------------------
class EmailLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    recipient_email = models.EmailField(max_length=200)
    send_timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} downloaded "{self.file.title}" to "{self.recipient_email}"'
    