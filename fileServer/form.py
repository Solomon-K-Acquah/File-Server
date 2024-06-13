from django import forms
from django.contrib.auth.models import User

# form to capture email to send the file
class SendEmailForm(forms.Form):
    email = forms.EmailField(
        max_length=100, 
        widget=forms.EmailInput(
            attrs={
                'class':'form-control', 
                'placeholder':'Enter your email'
                }
            )
        )
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'