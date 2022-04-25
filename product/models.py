from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=44)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
