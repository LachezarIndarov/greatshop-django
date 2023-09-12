from django.shortcuts import render
from store.models import Product, ReviewRating


def home(request):
    # products - Проверява всички продукти, който са налични или ги има в наличност
    products = Product.objects.all().filter(is_available = True).order_by('-created_date')

    # Get the reviews
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'review': reviews,
    }
    return render(request,'home.html', context)