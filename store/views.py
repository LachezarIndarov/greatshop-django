from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category


# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        # http://127.0.0.1:8000/store/shirts/
        # http://127.0.0.1:8000/store/jeans/
        # http://127.0.0.1:8000/store/shoes/
        #get_object_or_404(Category) - Bring categories is found, if don't found return 404 error
        # slug=category_slug    - е референция до папка category - models      (slug = models.SlugField(max_length=100, unique=True).Това ни доставя categories.
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()

    else:
        # All products
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        # __slug - sintax to take slug of this model
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,

    }

    return render(request, 'store/product_detail.html', context)
