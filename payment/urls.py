from django.urls import path
from .views import checkout_view, payment_process, payment_success, payment_cancelled, payment_webhook, confirm_payment, cancel_order_view

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('process/<int:order_id>/', payment_process, name='payment_process'),
    path('success/<int:order_id>/', payment_success, name='payment_success'),
    path('cancelled/', payment_cancelled, name='payment_cancelled'),
    path('webhook/', payment_webhook, name='payment_webhook'),
    path('confirm/', confirm_payment, name='confirm_payment'),
    path('cancel-order/<int:order_id>/', cancel_order_view, name='cancel_order'),
]