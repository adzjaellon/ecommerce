from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'user'


urlpatterns = [
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/', views.CustomerDetails.as_view(), name='customer-details'),
    path('<int:pk>/update/', views.CustomerUpdate.as_view(), name='customer-update'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('comment/delete/<int:pk>/', views.CommentDelete.as_view(), name='comment-delete'),
    path('comment/update/<int:pk>/', views.CommentUpdate.as_view(), name='comment-update'),
    path('orders/<int:pk>/', views.CustomerOrders.as_view(), name='customer-orders'),
    path('search-user/', views.UserSearch.as_view(), name='customer-search'),
    path('wishlist/<int:pk>/', views.WishlistDetails.as_view(), name='wishlist'),
    path('add-to-wishlist/', views.AddToWishlist.as_view(), name='add-to-wishlist'),
    path('remove-from-wishlist/', views.RemoveFromWishlist.as_view(), name='remove-from-wishlist'),
]
