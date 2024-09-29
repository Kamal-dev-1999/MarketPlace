from django.urls import path
from django import views
from .views import details , new_item , edit_item , delete , browse , view_items_category_wise , search_items
from django.conf import settings
from django.conf.urls.static import static

app_name = 'item'

urlpatterns = [
    path('',browse,name="browse"),
    path('<int:pk>/', details,name="detail"),
    path('new_item/',new_item,name="new"),
    path('<int:item_id>/',edit_item,name="edit"),
    path('<int:pk>/delete/',delete,name="delete"),
    path('category_wise/<int:category_id>/', view_items_category_wise, name="category-wise"),
    path('search-results/', search_items,name='search')
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
