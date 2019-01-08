from django.shortcuts import render
from django.template.loader import get_template
# Create your views here.
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse
from django.conf import settings





'''
test django paypal
'''
'''
def pay_process(request):

    # host = request.get_host()
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "10000000.00",
        'currency_code': 'NTD',
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('my_return_view')),
        "cancel_return": request.build_absolute_uri(reverse('my_cancel_view')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "apps/payment.html", context)

def my_return_view(request):
    return HttpResponse('<h1>This is my return view</h1>')

def my_cancel_view(request):
    return HttpResponse('<h1>This is my cancel view</h1>')
'''