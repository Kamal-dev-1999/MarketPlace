from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileCreateView,
    UserLogoutView,
    UserProfileListView,
    LandingPageView,
    HomePageView,
    OTPVerificationView,
    profile_form_view,
    RequestPasswordReset,
    OTPVerificationForResetPasswordView,
    PasswordResetFormView,
    # UserDeleteView,
    UserDeleteConfirmationView
)

urlpatterns = [
    path('user-landingpage', LandingPageView.as_view(), name='landingpage'),
    path('user-home/', HomePageView.as_view(), name='homepage'),
    path('user-register/', UserRegistrationView.as_view(), name='registeruser'),
    path('user-login/', UserLoginView.as_view(), name='loginuser'),
    path('otp-verify/', OTPVerificationView.as_view(), name='otp-verify'),
    path('user-profile-form/', profile_form_view, name='userprofile-create'),
    path('user-profile-create/', UserProfileCreateView.as_view(), name="profile-detail"),  # Fixed typo here
    path('userprofile/',UserProfileListView.as_view(),name="userprofile"),
    path('user-logout/', UserLogoutView.as_view(), name='logoutuser'),
    path('request-reset/', RequestPasswordReset.as_view(), name='request-reset'),
    path('otp-pass-reset/', OTPVerificationForResetPasswordView.as_view(), name='otp-passreset-verify'),
    path('password-reset-form/', PasswordResetFormView.as_view(), name='password-reset-form'),
    # path('delete-user/', UserDeleteView.as_view(), name='delete-user'),
    path('delete-user/', UserDeleteConfirmationView.as_view(), name='delete-user-confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
