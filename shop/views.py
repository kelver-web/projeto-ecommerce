from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

# Create your views here.


def product_list(request, slug_category=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if slug_category:
        category = get_object_or_404(Category, slug=slug_category)
        products = products.filter(category=category)

    context = {'category': category, 'products': products, 'categories': categories}
    return render(request, 'shop/product/list.html', context=context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    cart_product_form = CartAddProductForm()

    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'shop/product/detail.html', context=context)