from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# form to capture email to send the file
class SendEmailForm(forms.Form):
    email = forms.EmailField(
        max_length=100, 
        widget=forms.EmailInput(
            attrs={
                'class':'form-control', 
                'placeholder':'Enter your email',
                }
            )
        )

# new form for login, signup etc using default django User model
class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder' : 'Enter username', 'class' : 'form-control shadow-sm'})
        self.fields['email'].widget.attrs.update({'placeholder' : 'Enter email', 'class' : 'form-control shadow-sm'})
        self.fields['password1'].widget.attrs.update({'placeholder' : 'Enter your password', 'class' : 'form-control shadow-sm'})
        self.fields['password2'].widget.attrs.update({'placeholder' : 'Repeat password', 'class' : 'form-control shadow-sm'})
    
    # custom vaildation for new user registration or signup form
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username = username)
        if new.count():
            raise forms.ValidationError("User already exist")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email = email)
        if new.count():
            raise forms.ValidationError("Email already exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2
