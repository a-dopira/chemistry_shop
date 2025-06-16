import json
import stripe
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from cart.cart import Cart

from store.models import Order, OrderItem
from .forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout_view(request):
    cart = Cart(request)

    if cart.is_empty():
        messages.warning(request, "Your cart is empty!")
        return redirect("cart_view")

    removed_items = cart.clean_cart()
    if removed_items > 0:
        messages.warning(
            request,
            f"{removed_items} item(s) were removed because they are no longer available.",
        )

    if not cart.has_available_items():
        messages.error(request, "No available items in your cart")
        return redirect("cart_view")

    initial_data = {}
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            initial_data = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "phone": profile.phone_number,
                "address": profile.address,
            }
        except:
            initial_data = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.total_amount = cart.get_total_cost()

            if request.user.is_authenticated:
                order.created_by = request.user

            order.payment_method = "stripe"
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["product"].price,
                )

            request.session["order_id"] = order.id

            return redirect("payment_process", order_id=order.id)

    else:
        form = OrderForm(initial=initial_data)

    context = {
        "cart": cart,
        "form": form,
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        "title": "Checkout",
    }

    return render(request, "payment/checkout.html", context)


def payment_process(request, order_id):

    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, created_by=request.user)
    else:
        order = get_object_or_404(Order, id=order_id)

    if order.total_amount <= 0:
        messages.error(request, "Order is empty")
        order.delete()
        return redirect("cart_view")

    if order.is_paid:
        messages.info(request, "This order is already paid")
        return redirect("payment_success", order_id=order.id)

    request.session["order_id"] = order.id

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),
            currency="usd",
            description=f"Order #{order.id}",
            metadata={
                "order_id": order.id,
                "customer_email": order.email,
            },
        )

        order.payment_intent = intent.id
        order.save()

        context = {
            "order": order,
            "client_secret": intent.client_secret,
            "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
            "title": "Payment",
        }

        return render(request, "payment/process.html", context)

    except stripe.error.StripeError as e:
        messages.error(request, f"Payment error: {str(e)}")
        return redirect("checkout")


@csrf_exempt
def payment_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        try:
            order = Order.objects.get(payment_intent=payment_intent["id"])
            if not order.is_paid:
                _complete_order_payment(order)
        except Order.DoesNotExist:
            pass

    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        try:
            order = Order.objects.get(payment_intent=payment_intent["id"])
            if order.status != "cancelled":
                order.status = "cancelled"
                order.save()
        except Order.DoesNotExist:
            pass

    elif event["type"] == "charge.refunded":
        charge = event["data"]["object"]
        payment_intent_id = charge.get("payment_intent")
        if payment_intent_id:
            try:
                order = Order.objects.get(payment_intent=payment_intent_id)
                if order.status != "cancelled":
                    order.status = "cancelled"
                    order.is_paid = False
                    for item in order.items.all():
                        product = item.product
                        product.quantity += item.quantity
                        product.save()
                    order.save()
            except Order.DoesNotExist:
                pass

    return HttpResponse(status=200)


def _complete_order_payment(order):
    if order.is_paid:
        return

    order.is_paid = True
    order.paid_amount = order.total_amount
    order.status = "processing"
    order.payment_method = "stripe"
    order.save()

    for item in order.items.all():
        product = item.product
        if product.quantity >= item.quantity:
            product.quantity -= item.quantity
            product.save()


def payment_success(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(
            Order, id=order_id, created_by=request.user, is_paid=True
        )
    else:
        order = get_object_or_404(Order, id=order_id, is_paid=True)

    cart = Cart(request)
    cart.clear()

    if "order_id" in request.session:
        del request.session["order_id"]

    context = {"order": order, "title": "Payment Successful"}

    return render(request, "payment/success.html", context)


def payment_cancelled(request):

    context = {"title": "Payment Cancelled"}
    return render(request, "payment/cancelled.html", context)


@require_POST
def confirm_payment(request):
    try:
        data = json.loads(request.body)
        payment_intent_id = data.get("payment_intent_id")

        if not payment_intent_id:
            return JsonResponse({"error": "Payment Intent ID is required"}, status=400)

        intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        if intent.status == "succeeded":
            try:
                order = Order.objects.get(payment_intent=payment_intent_id)
                if not order.is_paid:
                    _complete_order_payment(order)

                return JsonResponse(
                    {
                        "success": True,
                        "redirect_url": reverse("payment_success", args=[order.id]),
                    }
                )

            except Order.DoesNotExist:
                return JsonResponse({"error": "Order not found"}, status=404)
        else:
            return JsonResponse({"error": "Payment not completed"}, status=400)

    except (json.JSONDecodeError, stripe.error.StripeError, Exception) as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
@require_POST
@transaction.atomic
def cancel_order_view(request, order_id):
    """Отмена заказа с возвратом средств"""
    order = get_object_or_404(Order, id=order_id, created_by=request.user)

    if order.status == "cancelled":
        if request.headers.get("HX-Request"):
            return HttpResponse(
                '<div class="error-message">Order is already cancelled.</div>'
            )
        messages.warning(request, "Order is already cancelled.")
        return redirect("user_account")

    if order.status in ["shipped", "delivered"]:
        if request.headers.get("HX-Request"):
            return HttpResponse(
                '<div class="error-message">Cannot cancel shipped/delivered order.</div>'
            )
        messages.error(request, "Cannot cancel shipped/delivered order.")
        return redirect("user_account")

    refund_id = None

    if order.is_paid and order.status == "processing":
        try:
            sid = transaction.savepoint()

            if order.payment_intent:
                refund = stripe.Refund.create(
                    payment_intent=order.payment_intent, reason="requested_by_customer"
                )

                if refund.status not in ["pending", "succeeded"]:
                    transaction.savepoint_rollback(sid)
                    if request.headers.get("HX-Request"):
                        return HttpResponse(
                            '<div class="error-message">Refund failed.</div>'
                        )
                    messages.error(request, "Refund failed. Contact support.")
                    return redirect("user_account")

                refund_id = refund.id
                order.refund_id = refund_id

        except stripe.error.StripeError as e:
            transaction.savepoint_rollback(sid)
            if request.headers.get("HX-Request"):
                return HttpResponse(
                    f'<div class="error-message">Error processing refund: {str(e)}</div>'
                )
            messages.error(request, "Error processing refund. Contact support.")
            return redirect("user_account")

    order.status = "cancelled"
    order.save()

    if order.is_paid:
        for item in order.items.all():
            product = item.product
            product.quantity += item.quantity
            product.save()

    if order.is_paid and "sid" in locals():
        transaction.savepoint_commit(sid)

    if refund_id:
        success_message = (
            f"Order cancelled and refund initiated. Refund ID: {refund_id}"
        )
    else:
        success_message = "Order cancelled successfully."

    if request.headers.get("HX-Request"):
        return render(
            request,
            "userprofile/partials/order_card.html",
            {"order": order, "success_message": success_message},
        )
    else:
        if refund_id:
            messages.success(
                request, f"Order cancelled and refund initiated. Refund ID: {refund_id}"
            )
        else:
            messages.success(request, "Order cancelled successfully.")

        return redirect("user_account")
