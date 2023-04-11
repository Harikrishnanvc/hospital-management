import json

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from users.models import LoginCredentials, BookAppointment
from .constants import PaymentStatus
from .models import Order


def order_payment(request, pk):
    if request.method == "GET":
        try:
            booking_name = LoginCredentials.objects.get(username=request.user)
            amount = 150
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create(
                {"amount": amount * 100, "currency": "INR", "payment_capture": "1"}
            )
            order = Order.objects.create(
                booking_name=booking_name, amount=amount, provider_order_id=razorpay_order["id"]
            )
            return render(
                request,
                "payment/payment.html",
                {
                    "callback_url": "http://" + "127.0.0.1:8000" + f"/callback/{pk}",
                    "razorpay_key": settings.RAZORPAY_KEY_ID,
                    "order": order,
                },
            )
        except LoginCredentials.DoesNotExist:
            return redirect('dashboard')

    return render(request, "payment/payment.html")


@csrf_exempt
def callback(request, pk):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.status = PaymentStatus.SUCCESS
        order.save()
        BookAppointment.objects.filter(id=pk).update(booking_status=True)

        return render(request, "payment/callback.html", context={"status": order.status})

    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "payment/callback.html", context={"status": order.status})
