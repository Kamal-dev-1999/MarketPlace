from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from E_shop.views import home_page, contact


urlpatterns = [
    path('', home_page, name='home'),
    path('contact/', contact, name="contact"),
] 

