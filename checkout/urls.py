from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('<price>/<pk>/', views.PaymentView.as_view(), name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]
