import email
from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User
from allauth.account.forms import LoginForm, SignupForm

# form to capture email to send the file
class SendEmailForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email'}))

# Custom login form to use email for login in allauth
# class CustomLoginForm(LoginForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['login'].labels = 'Email'
#         self.fields['login'].widget.attrs['placeholder'] = 'Your email'
        
        
# class CustomSignupForm(SignupForm):
#     username = forms.CharField(max_length=30, label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(max_length=100, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(max_length=100, label='Email', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(max_length=100, label='Email', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     # Add other custom fields here

#     def save(self, request):
#         user = super().save(request)
#         user.username = self.cleaned_data.get("username")
#         user.email = self.cleaned_data.get("email")
#         user.password1 = self.cleaned_data.get("password1")
#         user.password2 = self.cleaned_data.get("password2")
#         # Save other custom fields here
#         user.save()
#         return user

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
#         # self.fields.items():field.widget.attrs['class'] = 'form-control'

# class CustomSignupForm(SignupForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'class': 'form-control'})
#         self.fields['email'].widget.attrs.update({'class': 'form-control'})
#         self.fields['password1'].widget.attrs.update({'class': 'form-control'})
#         self.fields['password2'].widget.attrs.update({'class': 'form-control'})



# class CustomLoginForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'placeholder' : 'Enter username', 'class' : 'form-control shadow-sm'})
#         self.fields['email'].widget.attrs.update({'placeholder' : 'Enter email', 'class' : 'form-control shadow-sm'})
#         self.fields['password'].widget.attrs.update({'placeholder' : 'Enter your password', 'class' : 'form-control shadow-sm'})
#         self.fields['password2'].widget.attrs.update({'placeholder' : 'Repeat password', 'class' : 'form-control shadow-sm'})
    
#     # custom vaildation for new user registration or signup form
#     def clean_username(self):
#         username = self.cleaned_data['username'].lower()
#         new = User.objects.filter(username = username)
#         if new.count():
#             raise forms.ValidationError("User already exist")
#         return username

#     def clean_email(self):
#         email = self.cleaned_data['email'].lower()
#         new = User.objects.filter(email = email)
#         if new.count():
#             raise forms.ValidationError("Email already exist")
#         return email

#     def clean_password2(self):
#         password = self.cleaned_data['password']
#         password2 = self.cleaned_data['password2']
#         if password and password2 and password != password2:
#             raise forms.ValidationError("Password don't match")
#         return password2
    
# # User login form
# class LoginForm(AuthenticationForm):
#     email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder' : 'Email'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder' : 'Password'}))
