from .models import Category

def menu_links(request):
    links = Category.objects.all()  # We need all Category
    return dict(links=links) # We will bring all categories list and will be all stored in "links" variable