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
