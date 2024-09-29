from django import forms
from .models import MyUser
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = MyUser
        fields = ['email', 'name', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError("Passwords do not match.")

        return cleaned_data


# LoginForm inherits from Django's forms.Form to create a basic form for login.
class LoginForm(forms.Form):
    # Email field for user input. It uses EmailInput widget to ensure proper email input.
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    # Password field for user input. It uses PasswordInput widget to obscure the input.
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    # clean method is used to add custom validation logic for the form.
    def clean(self):
        # Call the parent class's clean method to get cleaned data.
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Add custom validation if needed (e.g., check for valid email format).
        # This example doesn't require additional validation, but this is where you would add it.

        # Return the cleaned data after performing any custom validations.
        return cleaned_data
    
    
class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Enter your email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address',
            'required': 'required'
        })
    )
    