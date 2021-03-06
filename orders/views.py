from code import interact
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
import datetime
import json
from carts.models import CartItem
from mystore.models import Product, Variation
from orders.models import Order, OrderProduct, Payment
from .forms import OrderForm
# Create your views here.


def payments(request):
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the carts items to order product table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # add product Variation in order product
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # Reduce the quantity of sold product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear data from cart item
    CartItem.objects.filter(user=request.user).delete()

    return render(request, 'orders/payments.html')

# Place order details


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If the cart count is less or equal zero, it should redirect to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_counts = cart_items.count()
    if cart_counts <= 0:
        return redirect('mystore')

    # For outside of form data--------------
    tax = 0
    grand_total = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (1*total)/100
    grand_total = total + tax
    # -------------------------------------

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            # Store all billing info inside the order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            # get user ip address
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%d%m%Y")  # 09/03/2022
            order_number = current_date + '-' + str(data.id)
            data.order_number = order_number
            data.save()

            # For payments
            order = Order.objects.get(
                user=current_user,  is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)

        else:
            return redirect('checkout')
