from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Order

@receiver(post_save, sender=Order)
@receiver(post_delete, sender=Order)
def invalidate_orders_cache(sender, instance, **kwargs):
    cache.delete('orders')
    cache.delete(f'order_{instance.id}')
