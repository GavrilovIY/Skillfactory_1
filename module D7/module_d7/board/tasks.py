from celery import shared_task
from .models import Order

@shared_task
def complete_order(oid):
    order = Order.objects.get(pk = oid)
    print('hello!!!')
    order.complete = True
    order.save()