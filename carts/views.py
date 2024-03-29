from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

# _cart_id - private function
def _cart_id(request):
    cart = request.session.session_key # We will take session id
    # if don't have session at all, we will create
    if not cart:
        cart = request.session.create()
    return cart # return the cart id

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) # get the product
    product_variation = []
    # we check  - if the user is authenticated
    if current_user.is_authenticated:

        if request.method == 'POST':
            # color = request.POST['color']
            # size = request.POST['size']
            # print(color, size)
            for item in request.POST:
                key = item
                value = request.POST[key]
                # print(key, value)
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    # print(variation)
                    product_variation.append(variation)
                except:
                    pass

        # size = request.GET['size']
        # return HttpResponse(color + ' ' + size)
        # exit()
        #     return HttpResponse(color)
        #     exit()

        # get the product - вземи продукта


        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)

            # if product_variation in existing_variation_list:
            #     return HttpResponse('true')
            # else:
            #     return HttpResponse('false')

            if product_variation in existing_variation_list:
                # increase the cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product = product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                # cart_item.quantity += 1
                item.save()

            # if len(product_variation) > 0:
            #     cart_item.variations.clear()
            #     for item in product_variation:
            #         cart_item.variations.add(item)
            # # cart_item.quantity += 1
            # cart_item.save()
        # except CartItem.DoesNotExist:
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                # for item in product_variation:
                cart_item.variations.add(*product_variation)
            cart_item.save()
        # return HttpResponse(cart_item.quantity)
        # exit()
        return redirect('cart')

    # we check - if user is not authenticated
    else:
        if request.method == 'POST':
            # color = request.POST['color']
            # size = request.POST['size']
            # print(color, size)
            for item in request.POST:
                key = item
                value = request.POST[key]
                # print(key, value)
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    # print(variation)
                    product_variation.append(variation)
                except:
                    pass

        # size = request.GET['size']
        # return HttpResponse(color + ' ' + size)
        # exit()
        #     return HttpResponse(color)
        #     exit()

        # get the product - вземи продукта

        try:
            # get the cart using the cart_id present in the browser session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        # try:
        if is_cart_item_exists:
            # This bring cart item
            # cart_item = CartItem.objects.get(product=product, cart=cart)
            # cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation   -> product_variation
            # item_id             -> database
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            print(existing_variation_list)

            # if product_variation in existing_variation_list:
            #     return HttpResponse('true')
            # else:
            #     return HttpResponse('false')

            if product_variation in existing_variation_list:
                # increase the cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product = product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                # cart_item.quantity += 1
                item.save()

            # if len(product_variation) > 0:
            #     cart_item.variations.clear()
            #     for item in product_variation:
            #         cart_item.variations.add(item)
            # # cart_item.quantity += 1
            # cart_item.save()
        # except CartItem.DoesNotExist:
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                # for item in product_variation:
                cart_item.variations.add(*product_variation)
            cart_item.save()
        # return HttpResponse(cart_item.quantity)
        # exit()
        return redirect('cart')

#Тази функция премахва с "минус" бутона една бройка от артикула
def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        # Намаляне на бройките в http://127.0.0.1:8000/cart/ с бутона за минуса
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

#Тази функция премахва незабавно с "remove" бутона целия артикул, независимо колко бройки има
def remove_cart_item(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete() # Тук се случва точно премахването
    return redirect('cart')



# def cart(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (20 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass #just ignore
#
#     # We send all context to HTML Template
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax'       : tax,
#         'grand_total': grand_total,
#     }
#
#     return render(request, 'store/cart.html', context)

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (20 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    # We send all context to HTML Template
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (20 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    # We send all context to HTML Template
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/checkout.html', context)