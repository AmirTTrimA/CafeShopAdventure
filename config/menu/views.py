from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import MenuItem

def menu_view(request):
    return render(request, 'menu.html') 

def product_view(request):
    return render(request, 'product.html')

def search_view(request):
    return render(request, 'search.html')

def add_to_cart(request, item_id):
    """Add a menu item to the shopping cart stored in the session."""
    menu_item = get_object_or_404(MenuItem, id=item_id)

    # Check if the cart exists in the session
    if 'cart' not in request.session:
        request.session['cart'] = {}  # Initialize an empty cart

    # Add or update the item in the cart
    if str(item_id) in request.session['cart']:
        request.session['cart'][str(item_id)] += 1  # Increase quantity
    else:
        request.session['cart'][str(item_id)] = 1  # Add new item

    request.session.modified = True  # Mark the session as modified

    messages.success(request, f"{menu_item.name} has been added to your cart.")
    return redirect('cart_view')

def cart_view(request):
    """Display the contents of the shopping cart."""
    cart = request.session.get('cart', {})
    menu_items = MenuItem.objects.filter(id__in=cart.keys())  # Get menu items in the cart
    return render(request, "cart.html", {"menu_items": menu_items, "cart": cart})

def clear_cart(request):
    """Clear the shopping cart from the session."""
    if 'cart' in request.session:
        del request.session['cart']  # Remove the cart from the session
        messages.success(request, "Your cart has been cleared.")
    return redirect('cart_view')

def search_product(request):
    query = request.GET.get('q')  # دریافت رشته جستجو از کاربر
    results = []
    
    if query:
        # جستجو در محصولات بر اساس نام و دسته‌بندی
        results = MenuItem.objects.filter(name__icontains=query) | MenuItem.objects.filter(category__icontains=query)
    if not results:
        messages.warning(request, "No results found.")        

    return render(request, 'search_results.html', {'results': results})
