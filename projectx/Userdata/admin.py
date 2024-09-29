from django.contrib import admin
from .models import MyUser

# Register MyUser model with the admin site
@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name','password')  # Fields to display in the admin list view
    search_fields = ('email', 'name')  # Fields to search in the admin interface
