
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls', namespace='product')),
    path('user/', include('user.urls', namespace='user')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('paypal/', include("paypal.standard.ipn.urls")),
]
