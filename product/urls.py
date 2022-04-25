from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'product'

urlpatterns = [
    path('', views.ProductList.as_view(), name='main-page'),
    path('create/', views.ProductCreate.as_view(), name='product-create')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
