from django.shortcuts import render, redirect 
from django.contrib.auth import logout
from items.models import Category, Item
from .forms import SignupForm


def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'marketplace/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'marketplace/contact.html')

def SignupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'marketplace/signup.html', {
        'form': form
    })
    
    
def logoutView(request):
    logout(request)
    return render(request, 'marketplace/index.html' )