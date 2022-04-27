from django.db import models
from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField()
    favourite = models.ManyToManyField('product.Product', blank=True)

    def __str__(self):
        return self.name

    @property
    def avatarURL(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url


TYPE = (
    ('Negative', 'Negative'),
    ('Positive', 'Positive')
)


class Comment(models.Model):
    author = models.ForeignKey(Customer, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='profile_comments')
    body = models.CharField(max_length=333)
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=8, choices=TYPE)

    def __str__(self):
        return f'{self.author} - {self.body}'
