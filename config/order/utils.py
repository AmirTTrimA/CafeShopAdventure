# utils.py
import json
from django.http import HttpResponse


def get_cart_from_cookies(request):
    """Retrieve the cart from cookies."""
    cart = request.COOKIES.get("cart")
    if cart:
        return json.loads(cart)
    return {}

# def str_to_dict(string):
#     # remove the curly braces from the string
#     string = string.strip('{}')

#     # split the string into key-value pairs
#     pairs = string.split(', ')

#     # use a dictionary comprehension to create
#     # the dictionary, converting the values to
#     # integers and removing the quotes from the keys
#     return {key[1:-2]: int(value) for key, value in (pair.split(': ') for pair in pairs)}

def set_cart_in_cookies(response, cart):
    """Set the cart in cookies."""
    response.set_cookie("cart", cart, max_age=60 * 60 * 24 * 30)
    return response
