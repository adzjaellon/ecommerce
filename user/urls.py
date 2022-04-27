from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'user'


urlpatterns = [
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/', views.CustomerDetails.as_view(), name='customer-details')
]
