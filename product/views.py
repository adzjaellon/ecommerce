from django.shortcuts import reverse
from .models import Product
from .forms import ProductCreateForm
from django.views.generic import ListView, CreateView


class ProductList(ListView):
    model = Product
    template_name = 'product/main.html'
    context_object_name = 'products'


class ProductCreate(CreateView):
    model = Product
    template_name = 'product/product_create.html'
    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse('product:main-page')
