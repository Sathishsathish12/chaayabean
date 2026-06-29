from django.shortcuts import render, redirect
from .models import Product, Order, Cart
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/')

@login_required
def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        item.item_total = item.product.price * item.quantity
        total += item.item_total

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity
        )

    cart_items.delete()

    return render(request, 'checkout_success.html')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })