from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderItem

def home(request):
    products = Product.objects.all().order_by("name")
    return render(request, "shop/home.html", {"products": products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "shop/product_detail.html", {"product": product})

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_data = request.session.get("cart", {})
    key = str(product.id)
    qty = int(cart_data.get(key, 0)) + 1
    if qty > product.stock:
        messages.error(request, "Requested quantity is not available in stock.")
    else:
        cart_data[key] = qty
        request.session["cart"] = cart_data
        messages.success(request, f"{product.name} added to cart.")
    return redirect(request.POST.get("next") or "home")

def cart(request):
    cart_data = request.session.get("cart", {})
    items, total = [], Decimal("0.00")
    products = Product.objects.filter(id__in=[int(k) for k in cart_data.keys()]) if cart_data else []
    for product in products:
        qty = int(cart_data.get(str(product.id), 0))
        subtotal = product.price * qty
        items.append({"product": product, "quantity": qty, "subtotal": subtotal})
        total += subtotal
    return render(request, "shop/cart.html", {"items": items, "total": total})

@require_POST
def update_cart(request, product_id):
    cart_data = request.session.get("cart", {})
    key = str(product_id)
    try:
        qty = int(request.POST.get("quantity", "1"))
    except ValueError:
        qty = 1
    product = get_object_or_404(Product, pk=product_id)
    if qty <= 0:
        cart_data.pop(key, None)
    elif qty <= product.stock:
        cart_data[key] = qty
    else:
        messages.error(request, "Quantity exceeds stock.")
    request.session["cart"] = cart_data
    return redirect("cart")

@login_required
def checkout(request):
    cart_data = request.session.get("cart", {})
    if request.method == "POST":
        if not cart_data:
            messages.error(request, "Your cart is empty.")
            return redirect("home")
        full_name = request.POST.get("full_name", "").strip()
        address = request.POST.get("address", "").strip()
        if not full_name or not address:
            messages.error(request, "Please enter your name and delivery address.")
            return redirect("checkout")
        products = Product.objects.filter(id__in=[int(k) for k in cart_data.keys()])
        total = sum((p.price * int(cart_data.get(str(p.id), 0)) for p in products), Decimal("0.00"))
        order = Order.objects.create(user=request.user, full_name=full_name, address=address, total=total)
        for product in products:
            qty = int(cart_data.get(str(product.id), 0))
            if qty:
                if qty > product.stock:
                    order.delete()
                    messages.error(request, f"Not enough stock for {product.name}.")
                    return redirect("cart")
                OrderItem.objects.create(order=order, product=product, quantity=qty, unit_price=product.price)
                product.stock -= qty
                product.save(update_fields=["stock"])
        request.session["cart"] = {}
        messages.success(request, f"Order #{order.id} placed successfully. Demo checkout only; no payment was taken.")
        return redirect("orders")
    return render(request, "shop/checkout.html", {"cart_count": sum(int(v) for v in cart_data.values())})

@login_required
def orders(request):
    return render(request, "shop/orders.html", {"orders": Order.objects.filter(user=request.user).prefetch_related("items").order_by("-created_at")})

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("home")
    return render(request, "shop/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username", ""), password=request.POST.get("password", ""))
        if user is not None:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid username or password.")
    return render(request, "shop/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")
