# payment/urls.py
from django.urls import path
from .views import CreatePaymentView, PaymentReturnView

urlpatterns = [
    path('create_payment/', CreatePaymentView.as_view(), name='create_payment'),
    path('vnpay_return/', PaymentReturnView.as_view(), name='vnpay_return'),
]
