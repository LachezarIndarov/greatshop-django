from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)


    # Променяме или преправяме името в  http://127.0.0.1:8000/admin/ - админ панела от Categoryes на Categories
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # Тази функция get_url ни дава URL на определена категория (All category - Shirts; All category - T Shirt; All category - Shoes; All category - Jeans; All category - Jackets )
    # args=[self.slug]) - Взима ни slug-а на категорията (Category - slug)
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
