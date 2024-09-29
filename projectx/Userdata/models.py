from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Custom user model
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# UserProfile model related to MyUser
class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    dob = models.DateField(verbose_name="Date of Birth", default=None)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    profile_img = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.CharField(max_length=500)

    def __str__(self):
        return self.full_name


# Password Reset model
class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset request for {self.email} at {self.created_at}"
