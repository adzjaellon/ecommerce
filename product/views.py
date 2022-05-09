from django.shortcuts import reverse, render, HttpResponseRedirect, get_object_or_404, redirect
from .models import Product, OrderItem, Order
from .forms import ProductCreateForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView,View
from django.contrib.auth.mixins import LoginRequiredMixin


# product


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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product/product_update.html'
    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse('product:product-details', kwargs={'pk': self.get_object().pk})


# cart


class CartView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.items.all()
        context = {
            'items': items,
            'order': order
        }
        return render(request, 'cart.html', context)


class AddToCart(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        customer = request.user.customer
        product_pk = request.POST.get('product_pk')
        number = request.POST.get('number')

        if int(number) > 0:
            product = get_object_or_404(Product, pk=product_pk)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order_item, created = OrderItem.objects.get_or_create(product=product, order=order)

            order_item.quantity += int(number)
            order_item.save()

        return redirect('product:basket')


class UpdateCartQuantity(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        remove = request.POST.get('remove', None)
        add = request.POST.get('add', None)

        if remove is not None:
            item = OrderItem.objects.get(pk=remove)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

        elif add is not None:
            item = OrderItem.objects.get(pk=add)
            item.quantity += 1
            item.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteFromCart(LoginRequiredMixin, DeleteView):
    model = OrderItem

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('product:basket')
