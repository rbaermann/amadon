from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    if "grandTotal" not in request.session:
        request.session["grandTotal"] = 0

    quantity_from_form = int(request.POST["quantity"])
    price = Product.objects.get(id = request.POST["product"]).price
    total_charge = quantity_from_form * price
    print("Charging credit card...")

    newOrder = Order(
        quantity_ordered = quantity_from_form,
        total_price = total_charge
    )
    newOrder.save()


    return redirect(f"/overview/{newOrder.id}")

def overview(request, orderId):
    orders = Order.objects.all()
    sum = 0
    for order in orders:
        sum += order.total_price

    checkoutDict = {
        "order" : Order.objects.get(id = orderId),
        "grandTotal" : sum
    }

    return render(request, "store/checkout.html", checkoutDict)