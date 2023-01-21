from django import template
from store_app.models import Order
register = template.Library()

@register.filter
def cart_count(user):
    if user.is_authenticated:
        cart_counts = Order.objects.filter(user=user, ordered=False)
        if cart_counts.exists():
            return cart_counts[0].cart_product.count()
        return 0
    return 0

