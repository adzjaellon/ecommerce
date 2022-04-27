from django.shortcuts import render
from django.views.generic import DetailView
from .models import Customer
from django.views.generic.edit import FormMixin
from .forms import CommentCreateForm


class CustomerDetails(FormMixin, DetailView):
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
        context['user'] = customer.user
        return context

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.customer
        form.instance.receiver = self.get_object()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')