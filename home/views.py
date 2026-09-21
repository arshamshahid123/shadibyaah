from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, ProductImage, ProductOption, Order, OrderItem
from decimal import Decimal

def home(request):
    return render(request, 'home/index.html')


def categories(request):
    products = Product.objects.all()
    return render(request, 'categories.html', {'products': products})

def mehndi_favors(request):
    products = Product.objects.filter(category='mehndi_favors')
    return render(request, 'mehndi_favors.html', {'products': products})
def wedding_favours(request):
    products = Product.objects.filter(category='wedding_favours')
    return render(request, 'wedding_favours.html', {'products': products})
def nikah_essentials(request):
    products = Product.objects.filter(category='nikah_essentials')
    return render(request, 'nikah_essentials.html', {'products': products})
def bridal_shower(request):
    products = Product.objects.filter(category='bridal_shower')
    return render(request, 'bridal_shower.html', {'products': products})
def baby_shower(request):
    products = Product.objects.filter(category='baby_shower')
    return render(request, 'baby_shower.html', {'products': products})
def wedding_cards(request):
    products = Product.objects.filter(category='wedding_cards')
    return render(request, 'wedding_cards.html', {'products': products})
def floral_jewellery(request):
    products = Product.objects.filter(category='floral_jewellery')
    return render(request, 'floral_jewellery.html', {'products': products})
def engagement(request):
    products = Product.objects.filter(category='engagement')
    return render(request, 'engagement.html', {'products': products})
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # Customization validation
    if product.customization_type == 'full':
        required_fields = [
            'bride_name',
            'groom_name',
            'event_type',
            'event_date'
        ]

        for field in required_fields:
            if not request.POST.get(field, '').strip():
                messages.error(request, 'Please fill in all required customization fields.')
                return redirect('product_detail', product_id=product.id)

    elif product.customization_type == 'name_only':
        if not request.POST.get('bride_name', '').strip():
            messages.error(request, 'Please fill in all required customization fields.')
            return redirect('product_detail', product_id=product.id)
    selected_option_id = request.POST.get('selected_option', '')

    selected_option = None

    if selected_option_id:
        selected_option = ProductOption.objects.get(
            id=selected_option_id,
            product=product
        )

    # Agar product option select hua hai
    if selected_option:
        item_price = selected_option.price
        option_name = selected_option.option_name

    # Agar product mein option nahi hai
    else:
        item_price = product.price
        option_name = ''

    # Product ki first image
    image = product.images.first()

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id]['quantity'] += 1

        # Latest product information
        cart[product_id]['name'] = product.name
        cart[product_id]['image'] = image.image if image else ''
        cart[product_id]['price'] = str(item_price)
        cart[product_id]['selected_option'] = option_name

        cart[product_id]['bride_name'] = request.POST.get(
            'bride_name', ''
        )

        cart[product_id]['groom_name'] = request.POST.get(
            'groom_name', ''
        )

        cart[product_id]['event_type'] = request.POST.get(
            'event_type', ''
        )

        cart[product_id]['event_date'] = request.POST.get(
            'event_date', ''
        )

        cart[product_id]['additional_information'] = request.POST.get(
            'additional_information', ''
        )

    else:

        cart[product_id] = {
            'name': product.name,
            'image': image.image if image else '',
            'price': str(item_price),
            'selected_option': option_name,
            'quantity': 1,

            'bride_name': request.POST.get(
                'bride_name', ''
            ),

            'groom_name': request.POST.get(
                'groom_name', ''
            ),

            'event_type': request.POST.get(
                'event_type', ''
            ),

            'event_date': request.POST.get(
                'event_date', ''
            ),

            'additional_information': request.POST.get(
                'additional_information', ''
            ),
        }

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')
def cart(request):
    cart = request.session.get('cart', {})

    total = 0

    for item in cart.values():
        item['subtotal'] = float(item['price']) * item['quantity']
        total += item['subtotal']

    return render(request, 'cart.html', {
        'cart': cart,
        'total': total
    })
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')
def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        if action == 'increase':
            cart[product_id]['quantity'] += 1

        elif action == 'decrease':
            cart[product_id]['quantity'] -= 1

            if cart[product_id]['quantity'] <= 0:
                del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    subtotal = Decimal('0.00')

    for item in cart.values():
        subtotal += Decimal(str(item['price'])) * item['quantity']

    delivery_charges = Decimal('350.00')
    total = subtotal + delivery_charges

    if request.method == 'POST':

        full_name = request.POST.get('full_name', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        delivery_address = request.POST.get('delivery_address', '').strip()
        additional_information = request.POST.get(
            'additional_information', ''
        ).strip()
        payment_method = request.POST.get('payment_method', '')
        payment_reference = request.POST.get('payment_reference', '')


        order = Order.objects.create(
            full_name=full_name,
            contact_number=contact_number,
            delivery_address=delivery_address,
            additional_information=additional_information,
            subtotal=subtotal,
            delivery_charges=delivery_charges,
            total_amount=total,
            payment_method=payment_method,
            payment_reference=payment_reference,
        )

        for item in cart.values():

            item_subtotal = (
                Decimal(str(item['price'])) * item['quantity']
            )

            OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                selected_option=item.get('selected_option', ''),
                price=Decimal(str(item['price'])),
                quantity=item['quantity'],
                subtotal=item_subtotal,
                bride_name=item.get('bride_name', ''),
                groom_name=item.get('groom_name', ''),
                event_type=item.get('event_type', ''),
                event_date=item.get('event_date', ''),
                additional_information=item.get(
                    'additional_information', ''
                ),
            )

        return render(request, 'checkout.html', {
            'order_placed': True,
            'full_name': full_name,
        })

    return render(request, 'checkout.html', {
        'cart': cart,
        'subtotal': subtotal,
        'delivery_charges': delivery_charges,
        'total': total,
    })