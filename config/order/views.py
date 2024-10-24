from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, MenuItem, OrderItem, Customer
from django.utils import timezone
from datetime import timedelta

#  افزودن آیتم به سبد خرید
@login_required
def add_to_cart(request, item_id):
    """Add a menu item to the customer's cart."""
    menu_item = get_object_or_404(MenuItem, id=item_id)
    
    # اطمینان از اینکه کاربر مشتری است
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        messages.error(request, "You are not associated with a customer account.")  
        return redirect('menu')  
    
    # ایجاد یا گرفتن سبد خرید مشتری
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)

    # اگر آیتم قبلاً وجود داشت، تعداد آن را افزایش دهید
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{menu_item.name} has been added to your cart.")
    return redirect("cart_view")

# نمایش سبد خرید
@login_required
def cart_view(request):
    """Display the contents of the customer's cart."""
    try:
        cart = Cart.objects.get(customer=request.user.customer)
    except Cart.DoesNotExist:
        messages.warning(request, "You do not have any items in your cart.")  
        return redirect('menu') 

    return render(request, "cart.html", {"cart": cart})

#  ارسال سفارش
@login_required
def submit_order(request):
    """Submit an order based on the items in the customer's cart."""
    cart = get_object_or_404(Cart, customer=request.user.customer)

    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_view")

    # ایجاد یک سفارش جدید
    order = Order.objects.create(customer=request.user.customer)

    # افزودن آیتم‌های سبد خرید به سفارش
    for item in cart.items.all():
        order.cart_items.add(item)

    # محاسبه قیمت کل
    order.calculate_total_price()

    # خالی کردن سبد خرید پس از ثبت سفارش
    cart.items.all().delete()

    messages.success(request, "Your order has been submitted successfully!")
    return redirect("order_confirmation", order_id=order.id)

# مدیریت آیتم‌های سفارش توسط کاربران Staff
@login_required
def manage_order_items(request, order_id):
    """Allow staff to add or remove items from an order."""
    order = get_object_or_404(Order, id=order_id)

    # اطمینان از اینکه کاربر یک عضو staff است
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to manage this order.")
        return redirect("order_list")

    if request.method == "POST":
        if 'add_item' in request.POST:
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))

            menu_item = get_object_or_404(MenuItem, id=item_id)
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)

            messages.success(request, f"{menu_item.name} has been added to the order.")
        
        elif 'remove_item' in request.POST:
            item_id = request.POST.get('item_id')
            order_item = get_object_or_404(OrderItem, id=item_id, order=order)
            order_item.delete()

            messages.success(request, f"{order_item.menu_item.name} has been removed from the order.")

        return redirect('manage_order_items', order_id=order.id)

    order_items = order.cart_items.all()
    return render(request, "manage_order_items.html", {"order": order, "order_items": order_items})

# تغییر وضعیت سفارش
@login_required
def change_order_status(request, order_id):
    """Allow staff to change the status of an order."""
    order = get_object_or_404(Order, id=order_id)

    # اطمینان از اینکه کاربر یک عضو staff است
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to change the status of this order.")
        return redirect("order_list")

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f"The status of Order {order.id} has been changed to {new_status}.")
        else:
            messages.error(request, "Invalid status selected.")

        return redirect('order_list')

    return render(request, "change_order_status.html", {"order": order})

# فرآیند Checkout (پرداخت)
@login_required
def checkout(request):
    """Handle the checkout process, calculating the total price and creating an order."""
    customer_cart = get_object_or_404(Cart, customer=request.user.customer)

    if customer_cart.items.count() == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_view")

    total_price = customer_cart.get_total_price()

    if request.method == "POST":
        order = Order.objects.create(customer=request.user.customer)
        for item in customer_cart.items.all():
            order.cart_items.add(item)

        order.calculate_total_price()
        order.status = "Pending"
        order.save()

        customer_cart.items.all().delete()

        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {'cart': customer_cart, 'total_price': total_price})
    
# تأیید سفارش
@login_required
def order_confirmation(request, order_id):
    """Show the order confirmation after checkout."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

def order_status_cleanup(request):
    """Clean up old orders that are 'Canceled' or 'Completed'."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to clean up orders.")
        return redirect('order_list')
    
    # تعیین محدوده زمانی برای سفارش‌های قدیمی. مثلا سفارش‌هایی که بیش از 30 روز پیش ایجاد شده‌اند
    time_threshold = timezone.now() - timedelta(days=30)

    # پیدا کردن سفارش‌هایی که وضعیت آنها 'Canceled' یا 'Completed' است و بیش از 30 روز پیش ایجاد شده‌اند
    old_orders = Order.objects.filter(
        status__in=['Canceled', 'Completed'], 
        created_at__lt=time_threshold
    )
    
    # حذف این سفارش‌ها
    deleted_count, _ = old_orders.delete()
    
    # نمایش پیغام به کاربر درباره تعداد سفارش‌های حذف شده
    messages.success(request, f"{deleted_count} old orders have been cleaned up.")
    
    return redirect('order_list')

@login_required
def change_item_quantity(request, order_id, item_id):
    """Allow staff to change the quantity of an item in an order."""
    
    # پیدا کردن سفارش و آیتم مربوطه
    order = get_object_or_404(Order, id=order_id)
    order_item = get_object_or_404(OrderItem, order=order, menu_item_id=item_id)
    
    # بررسی اینکه آیا کاربر یک عضو staff است
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to change item quantities in this order.")
        return redirect('order_list')

    if request.method == "POST":
        # دریافت مقدار جدید از فرم
        new_quantity = int(request.POST.get('quantity', 1))

        # بررسی اینکه مقدار جدید معتبر است
        if new_quantity > 0:
            order_item.quantity = new_quantity
            order_item.save()  # ذخیره آیتم با مقدار جدید
            messages.success(request, f"The quantity of {order_item.menu_item.name} has been updated to {new_quantity}.")
        else:
            messages.error(request, "Quantity must be greater than zero.")

        # محاسبه مجدد قیمت کل سفارش
        order.calculate_total_price()
        order.save()  # ذخیره سفارش با قیمت جدید

        return redirect('manage_order_items', order_id=order.id)

    return render(request, 'change_item_quantity.html', {'order': order, 'order_item': order_item})

@login_required
def submit_order(request):
    """Submit an order and add points based on the items in the order."""
    
    # دریافت سبد خرید مشتری
    cart = get_object_or_404(Cart, customer=request.user.customer)

    # بررسی خالی نبودن سبد خرید
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_view")

    # ایجاد یک سفارش جدید
    order = Order.objects.create(customer=request.user.customer)

    # مجموع امتیازات آیتم‌های سبد خرید
    total_points = 0

    # افزودن آیتم‌های سبد خرید به سفارش و محاسبه امتیازات
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order, 
            menu_item=item.menu_item, 
            quantity=item.quantity
        )
        # اضافه کردن امتیاز این آیتم به مجموع امتیازات
        total_points += item.menu_item.points * item.quantity

    # محاسبه قیمت کل سفارش
    order.calculate_total_price()

    # افزودن امتیاز به مشتری
    customer = request.user.customer
    customer.points += total_points
    customer.save()

    # خالی کردن سبد خرید پس از ثبت سفارش
    cart.items.all().delete()

    messages.success(request, f"Your order has been submitted successfully! You've earned {total_points} points.")
    return redirect("order_confirmation", order_id=order.id)