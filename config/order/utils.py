# utils.py
import json
from django.http import HttpResponse


def get_cart_from_cookies(request):
    cart = request.COOKIES.get("cart")
    if cart:
        return json.loads(cart)
    return {}


def set_cart_in_cookies(response, cart):
    response.set_cookie("cart", json.dumps(cart), max_age=60 * 60 * 24 * 30)  # 30 days
