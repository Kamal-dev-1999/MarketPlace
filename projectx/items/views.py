from django.shortcuts import render , get_object_or_404
from .models import Item , Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm
from django.db.models import Q
from django.shortcuts import redirect , render


# Create your views here.
@login_required
def browse(request):
    query = request.GET.get('query', '').strip().lower()
    category_id = request.GET.get('category', '0')  # Use string '0' for consistent type
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    print(f"Query: '{query}', Category ID: '{category_id}'")  # Debugging line

    if category_id and category_id != '0':
        items = items.filter(category_id=category_id)

    if query :
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'marketplace/browse.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id) if category_id != '0' else 0
    })

    
    
@login_required
def details(request,pk):
    item=get_object_or_404(Item, pk=pk) #the first pk is from the model that we will get and the next is the url one so the models object will only be displayed in the detail page of that object 
    related_items=Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk)[0:4]
    return render(request, 'marketplace/detail.html', context={
        'item': item,
        'related_items':related_items
    })
    
    

@login_required
def new_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item=form.save(commit=False)
            item.user=request.user
            item.save()
            return redirect('item:detail',pk=item.pk)
    else:
        form= NewItemForm()

    return render(request, 'marketplace/newitem.html', context={'form':form})
            
            
            
@login_required
def edit_item(request, item_id):
    # Get the item instance to edit, or show a 404 error if not found
    item = get_object_or_404(Item, id=item_id)
    
    # If the request is a POST, handle form submission
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('core:index')  # Redirect to your desired page after saving
    else:
        # If the request is a GET (or any other method), populate the form with the item's existing data
        form = NewItemForm(instance=item)
    
    # Render the template with the form
    return render(request, 'marketplace/newitem.html', {'form': form, 'item': item})




@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')          




# @login_required
# def view_items_category_wise(request):
#     category_id = request.GET.get('category')  # Get category from query parameters
#     items = Item.objects.filter(category_id=category_id) if category_id else Item.objects.all()
#     return render(request, 'marketplace/items.html', {'items': items})


@login_required
def view_items_category_wise(request, category_id):
    items = Item.objects.filter(category__id=category_id)  # Filter items by category ID
    return render(request, 'marketplace/items.html', {'items': items})




def search_items(request):
    query = request.GET.get('q')  # Get search query from query parameters
    items = None
    if query:  # If a query exists
        # Filter items by name or description (case insensitive)
        items = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        # If no search query, return all items (optional)
        items = Item.objects.all()
    
    return render(request, 'marketplace/items.html', {'items': items, 'query': query})