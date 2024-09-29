from django.shortcuts import render
from items.models import Category , Item
# Create your views here.

def home_page(request):
   items = Item.objects.filter(is_sold=False)[0:6]
   categories = Category.objects.all()

   return render(request, 'marketplace/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'marketplace/contact.html')

