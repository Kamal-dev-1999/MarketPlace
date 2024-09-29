import bcrypt
from cryptography.fernet import Fernet
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import messages
import random
from .models import MyUser , UserProfile
from .forms import RegisterForm, LoginForm , ResetPasswordForm
import os
from .serializers import ResetPasswordRequestSerializer , UserProfileSerializer , UserSerializers
from rest_framework import generics
import logging
# Initialize AES encryption key from settings (set this securely in your environment variables)
from cryptography.fernet import Fernet
import bcrypt
from django.conf import settings
import base64
# Initialize the cipher suite for AES encryption/decryption
# Initialize logger
# Initialize logger
logger = logging.getLogger(__name__)

# Retrieve the AES key from settings
# Retrieve the AES key from settings
def get_cipher():
    # Ensure the key is in bytes; if it's stored as a string in settings, decode it first
    KEY = settings.AES_KEY.encode() if isinstance(settings.AES_KEY, str) else settings.AES_KEY
    return Fernet(KEY)


def encrypt_email(email):
    """
    Encrypts the given email and encodes it as a Base64 string.
    """
    if not isinstance(email, bytes):
        email = email.encode()

    # Use the cipher retrieved from get_cipher() to ensure key consistency
    cipher = get_cipher()
    encrypted = cipher.encrypt(email)
    
    # Encode to Base64 to make it JSON serializable
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_email(encrypted_email):
    """
    Decodes from Base64 and decrypts the given encrypted email.
    """
    # Decode from Base64 to get bytes
    encrypted_email_bytes = base64.urlsafe_b64decode(encrypted_email.encode())

    # Use the cipher to decrypt the bytes
    cipher = get_cipher()
    decrypted = cipher.decrypt(encrypted_email_bytes)
    return decrypted.decode()

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

from django.contrib.auth.hashers import check_password

def verify_password(password, hashed_password):
    """
    Verifies the password using Django's check_password utility.
    """
    return check_password(password, hashed_password)


# Home page view
class HomePageView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        print("User is authenticated:", request.user.is_authenticated)
        return render(request, 'userdata/jwt-auth/homepage.html', {'user': request.user})


def homepage(request):
    print("User is authenticated:", request.user.is_authenticated)
    return render(request, 'homepage.html')


# Landing page view
class LandingPageView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, 'userdata/jwt-auth/landingpage.html')

# Registration view
class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        form = RegisterForm()
        return render(request, 'userdata/jwt-auth/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Encrypt email and hash password
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            encrypted_email = encrypt_email(email)  # Assuming you need to encrypt email
            hashed_password = hash_password(password)  # This should be directly used by set_password

            # Create user with encrypted email and hashed password
            user = MyUser(email=encrypted_email)
            user.set_password(password)  # This automatically handles the password hashing
            user.save()

            return redirect('loginuser')  # Redirect to login page after registration

        return render(request, 'userdata/jwt-auth/register.html', {'form': form})


# Login view with OTP generation

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        form = LoginForm()
        return render(request, 'userdata/jwt-auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Encrypt email to find the user
            encrypted_email = encrypt_email(email)
            

            user = MyUser.objects.filter(email__exact=encrypted_email).first()

            if user is None:
                raise AuthenticationFailed("User does not exist")

            # Verify password
            if not user.check_password(password):  # Use Django's check_password method
                raise AuthenticationFailed("Incorrect password")

            # Generate OTP and send via email
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['email'] = email

            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect('otp-verify')  # Redirect to OTP verification

        return render(request, 'userdata/jwt-auth/login.html', {'form': form})




# OTP verification view
class OTPVerificationView(APIView):
    template_name = 'userdata/jwt-auth/otp_verify.html'
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        input_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        email = request.session.get('email')

        if str(input_otp) == str(session_otp):
            # Clear OTP after verification
            if 'otp' in request.session:
                del request.session['otp']

            # Redirect to profile form, where the user can set up their profile
            return redirect('profile-detail')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, self.template_name)

# View to display user profile form after OTP verification
def profile_form_view(request):
    # Retrieve the email from session
    email = request.session.get('email')
    if not email:
        return redirect('loginuser')  # Redirect if no email in session

    # Check if the user exists
    try:
        user = MyUser.objects.get(email=encrypt_email(email).decode())
    except MyUser.DoesNotExist:
        return redirect('loginuser')  # Redirect if user not found (extra validation)

    # Check if the user already has a profile
    if UserProfile.objects.filter(user=user).exists():
        return redirect('homepage')  # Redirect if profile already exists

    # Render the profile form if no profile exists
    return render(request, 'userdata/users/profile.html', {'email': email})

class UserProfileCreateView(APIView):
    permission_classes = [permissions.AllowAny]  # Adjust if needed

    def get_user_from_session(self, request):
        # Retrieve the email from session
        email = request.session.get('email')
        if not email:
            return None, {"error": "Email not found in session"}, status.HTTP_400_BAD_REQUEST
        
        try:
            user = MyUser.objects.get(email=encrypt_email(email).decode())
        except MyUser.DoesNotExist:
            return None, {"error": "User does not exist"}, status.HTTP_404_NOT_FOUND
        
        return user, None, None

    def get(self, request):
        # Retrieve the user from session
        user, error, status_code = self.get_user_from_session(request)
        if error:
            return Response(error, status=status_code)

        # Check if the user already has a profile
        profile_exists = UserProfile.objects.filter(user=user).exists()

        # Render template with profile_exists context
        return render(request, 'userdata/users/profile.html', {'profile_exists': profile_exists})

    def post(self, request):
        # Retrieve the user from session
        user, error, status_code = self.get_user_from_session(request)
        if error:
            return Response(error, status=status_code)

        # Check if the user already has a profile
        if UserProfile.objects.filter(user=user).exists():
            return redirect('homepage')  # Redirect if profile already exists

        # Prepare data for the serializer
        data = request.data.copy()
        data['user'] = user.pk  # Set user field to the primary key

        # Validate and save the profile
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            # Clear the email from session after successful profile creation
            if 'email' in request.session:
                del request.session['email']

            return redirect('homepage')  # Redirect to homepage on success

        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Display all user profiles
class UserProfileListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)  # Use the request.user instance
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

# User logout view
class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        response = Response({'message': "Successfully logged out! JWT has been deleted. Please log in again."})
        response.delete_cookie('jwt')
        return response

    def post(self, request):
        response = Response({'message': "Successfully logged out! Cookies have been deleted."})
        
        response.delete_cookie('jwt')
        return response

class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        user = MyUser.objects.filter(email__iexact=email).first()

        if user is None:
            form = ResetPasswordForm()
            messages.error(request, 'User with this email does not exist.')
            return render(request, 'userdata/jwt-auth/login.html', {'form': form})

        # Generate an OTP
        otp = random.randint(100000, 999999)

        # Encrypt the email before storing in the session
        encrypted_email = encrypt_email(email)
        request.session['otp'] = otp
        request.session['email'] = encrypted_email

        # Send OTP to user's email
        send_mail(
            'Your OTP for Password Reset',
            f'Your OTP is {otp}. Please enter it to reset your password.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        request.session.set_expiry(300)  # Session expires in 5 minutes
        return redirect('otp-passreset-verify')




class OTPVerificationForResetPasswordView(APIView):
    template_name = 'userdata/users/otp_verify.html'
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        input_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        email = request.session.get('email')

        if str(input_otp) == str(session_otp):
            # Clear OTP after verification
            if 'otp' in request.session:
                del request.session['otp']

            # Redirect to password reset form
            return redirect('password-reset-form')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, self.template_name)

class PasswordResetFormView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'userdata/users/password_reset_form.html', {'form': form})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the encrypted email from the session
        encrypted_email = request.session.get('email')
        logger.debug(f"Encrypted email retrieved from session: {encrypted_email}")

        # Validate encrypted_email
        if not encrypted_email or not isinstance(encrypted_email, str):
            logger.error("Invalid email in session.")
            return Response({'error': 'Invalid email in session.'}, status=status.HTTP_400_BAD_REQUEST)

        # Decrypt the email
        try:
            decrypted_email = decrypt_email(encrypted_email)
            logger.debug(f"Decrypted email: {decrypted_email}")
        except Exception as e:
            logger.error(f"Error decrypting email: {str(e)}")
            return Response({'error': f'Error decrypting email: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Find the user by decrypted email
        user = MyUser.objects.filter(email__iexact=decrypted_email).first()

        if user:
            new_password = serializer.validated_data.get('new_password')
            user.set_password(new_password)
            user.save()

            # Clear the email from the session after password reset
            if 'email' in request.session:
                del request.session['email']
            if 'otp' in request.session:
                del request.session['otp']

            return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        else:
            logger.error(f"User with email {decrypted_email} does not exist.")
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)