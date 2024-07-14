from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User  
from .models import *

@receiver(user_logged_in)
def move_cart_to_user(sender, user, request, **kwargs):
    session_cart_id = request.session.get('cart_id')
    if session_cart_id:
        session_cart = Cart.objects.get(id=session_cart_id)
        session_cart.user = user
        session_cart.save()

@receiver(user_logged_out)
def save_cart_in_session(sender, user, request, **kwargs):
    try:
        cart = Cart.objects.get(user=user)
        request.session['cart_id'] = cart.id
    except Cart.DoesNotExist:
        pass


