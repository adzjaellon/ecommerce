from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, UpdateView, View, DeleteView, ListView
from .models import Customer, Comment, Wishlist
from django.views.generic.edit import FormMixin
from .forms import CommentCreateForm, CustomerUpdateForm, UserRegisterForm, CommentUpdateForm
from django.shortcuts import reverse, redirect, HttpResponseRedirect
from product.models import Order, Product
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterUser(View):
    def post(self, request, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')

        return render(request, 'user/register_user.html')

    def get(self, request, **kwargs):
        form = UserRegisterForm()

        context = {
            'form': form
        }
        return render(request, 'user/register_user.html', context)


class CustomerDetails(LoginRequiredMixin, FormMixin, DetailView):
    model = Customer
    template_name = 'user/user_details.html'
    context_object_name = 'customer'
    form_class = CommentCreateForm

    def get_object(self, **kwargs):
        pk = self.kwargs['pk']
        obj = Customer.objects.get(pk=pk)
        return obj

    def get_context_data(self, **kwargs):
        customer = self.get_object()
        context = super().get_context_data(**kwargs)
        comment_customers = Customer.objects.filter(comment__receiver=customer)
        all_customer_opinions = customer.profile_comments.all().count()
        customer_positive_opinions = customer.profile_comments.filter(type='Positive').count()

        try:
            percent = (customer_positive_opinions / all_customer_opinions) * 100
        except Exception:
            percent = 0

        context['comments_customers'] = comment_customers
        context['user'] = customer.user
        context['opinion_number'] = all_customer_opinions
        context['percent'] = percent
        return context

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user.customer
        form.instance.receiver = self.get_object()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    template_name = 'user/user_update.html'
    context_object_name = 'customer'

    def get(self, request, *args, **kwargs):
        if request.user.customer != self.get_object():
            return redirect('product:main-page')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('user:customer-details', kwargs={'pk': self.get_object().pk})


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment

    def get(self, request, **kwargs):
        if request.user.customer != self.get_object().author:
            return reverse('user:customer-details', kwargs={'pk': self.get_object().receiver.pk})
        return self.post(request, **kwargs)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'comment/update.html'

    def get(self, request, *args, **kwargs):
        if request.user.customer != self.get_object().author:
            return redirect('product:main-page')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('user:customer-details', kwargs={'pk': self.get_object().receiver.pk})


class CustomerOrders(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'user/user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        pk = self.kwargs['pk']
        customer = get_object_or_404(Customer, pk=pk)
        orders = Order.objects.filter(customer=customer, complete=True).order_by('-ordered')
        return orders


class UserSearch(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.GET.get('user_search')

        if user:
            queryset = Customer.objects.filter(name__icontains=user)
            return render(request, 'user/user_search.html', context={'users': queryset})

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddToWishlist(View):
    def post(self, request, **kwargs):
        pk = request.POST.get('pk')
        print(pk)
        item = Product.objects.get(pk=pk)
        user = Customer.objects.get(user=request.user)
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        if item not in wishlist.products.all():
            wishlist.products.add(item)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RemoveFromWishlist(View):
    def post(self, request, **kwargs):
        pk = request.POST.get('pk')
        print(pk)
        item = Product.objects.get(pk=pk)
        user = Customer.objects.get(user=request.user)
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        wishlist.products.remove(item)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class WishlistDetails(LoginRequiredMixin, DetailView):
    model = Wishlist
    context_object_name = 'wishlist'
    template_name = 'user/user_wishlist.html'

    def get_object(self, queryset=None):
        print(self.kwargs)
        pk = self.kwargs['pk']
        user = get_object_or_404(Customer, pk=pk)
        obj, created = Wishlist.objects.get_or_create(user=user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_object().products.all()
        return context
