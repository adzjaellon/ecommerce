from django.shortcuts import reverse
from .models import Product
from .forms import ProductCreateForm
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductList(ListView):
    model = Product
    template_name = 'product/main.html'
    context_object_name = 'products'


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'product/product_create.html'
    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse('product:main-page')

    def form_valid(self, form):
        form.instance.seller = self.request.user.customer
        return super().form_valid(form)


class ProductDetails(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product/product-details.html'
    context_object_name = 'product'
