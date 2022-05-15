from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'product'


urlpatterns = [
    path('', views.ProductList.as_view(), name='main-page'),
    path('create/', views.ProductCreate.as_view(), name='product-create'),
    path('<int:pk>/details/', views.ProductDetails.as_view(), name='product-details'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('cart/', views.CartView.as_view(), name='basket'),
    path('add-to-cart/', views.AddToCart.as_view(), name='add-to-cart'),
    path('delete-from-cart/<int:pk>/', views.DeleteFromCart.as_view(), name='delete-from-cart'),
    path('update-quantity/', views.UpdateCartQuantity.as_view(), name='update-quantity'),
    path('order/<int:pk>/', views.OrderDetails.as_view(), name='order-details'),
    path('search/', views.ProductSearch.as_view(), name='search')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
