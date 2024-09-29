from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
import jwt
import datetime
from .models import MyUser, UserProfile
from .serializers import UserSerializers, UserProfileSerializer , ResetPasswordRequestSerializer
from .forms import RegisterForm, LoginForm
from rest_framework import generics
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import PasswordReset
import os

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
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
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
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = MyUser.objects.filter(email=email).first()
            if user is None:
                raise AuthenticationFailed("User does not exist")
            if not user.check_password(password):
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
            del request.session['otp']  # Clear OTP after verification
            request.session['email'] = email
            return redirect('profile-detail')  # Redirect to profile form
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, self.template_name)


# View to display user profile form after OTP verification
# View to display user profile form after OTP verification
def profile_form_view(request):
    # Retrieve the email from session
    email = request.session.get('email')
    if not email:
        return redirect('loginuser')  # Redirect if no email in session

    # Check if the user exists
    try:
        user = MyUser.objects.get(email=email)
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
            user = MyUser.objects.get(email=email)
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
        email = request.data.get('email')
        user = MyUser.objects.filter(email__iexact=email).first()
        if user is None:
            form=LoginForm()
            messages.error(request, 'User with this email does not exist.')
            return render(request, 'userdata/jwt-auth/login.html', {'form': form})
        if user:
            # Generate an OTP
            otp = random.randint(100000, 999999)

            # Store the OTP and email in the session
            request.session['otp'] = otp
            request.session['email'] = email

            # Send OTP to user's email
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is {otp}. Please enter it to reset your password.',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            request.session.set_expiry(300)
            # return Response({'success': 'We have sent you an OTP to reset your password'}, status=status.HTTP_200_OK)
            return redirect('otp-passreset-verify')
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        
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

            
            # Redirect to password reset form, where the user can set a new password
            return redirect('password-reset-form')  # Add the name of the URL where the user resets their password
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, self.template_name)
        
class PasswordResetFormView(APIView):
    template_name = 'userdata/users/password_reset_form.html'
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        new_password = request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')
        email = request.session.get('email')
        user = MyUser.objects.filter(email__iexact=email).first()
        if str(new_password)==str(confirm_password):
            if user:
                # Set the new password
                user.set_password(new_password)
                user.save()

                messages.success(request, 'Your password has been reset successfully.')
                return redirect('loginuser')  # Redirect to login after successful reset
            else:
                messages.error(request, 'Something went wrong. Please try again.')
                return render(request, self.template_name)
        else:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, self.template_name)
        
from django.contrib.auth import logout  
from rest_framework.permissions import IsAuthenticated  
from django.contrib.auth import get_user_model    
# View to delete user account
User = get_user_model()
# class UserDeleteView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         # Get the logged-in user
#         user = request.user

#         # Log out the user before deletion
#         logout(request)

#         # Delete the user account
#         user.delete()

#         # Send a success response
#         return redirect('homepage')
#     def get(self, request,*args, **kwargs):
#         # Get the logged-in user
#         user = request.user

#         # Log out the user before deletion
#         logout(request)

#         # Delete the user account
#         user.delete()

#         # Send a success response
#         return redirect('homepage')
    
class UserDeleteConfirmationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'userdata/jwt-auth/delete_account.html')

    def post(self, request):
        # Get the logged-in user
        user = request.user

        # Delete the related UserProfile first
        UserProfile.objects.filter(user=user).delete()

        # Log out the user before deletion
        logout(request)

        # Delete the user account
        user.delete()

        # Redirect to homepage after deletion
        return redirect('homepage')

