from django.db import models
from user.models import Customer


class Product(models.Model):
    name = models.CharField(max_length=44)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name='order')
    ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'Order - {self.customer} - {self.ordered}'

    @property
    def cart_value(self):
        items = self.items.all()
        value = sum(item.product.price * item.quantity for item in items)
        return value


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='items')
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.product.price}'
