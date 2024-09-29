
from django.urls import path
from  E_shop.views import contact
from . import views 
from .forms import LoginForm
from django.contrib.auth import views as auth_views 

app_name='core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', contact, name="contact"),
    path('signup/',views.SignupView,name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='marketplace/signin.html', authentication_form=LoginForm), name='login'),

    path('loggedout/',views.logoutView,name="logout")
]