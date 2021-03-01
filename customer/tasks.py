import string

from django.contrib.auth.models import User
from customer.models import TablestableInStore
from django.utils.crypto import get_random_string
from customer.models import Meat, OrderReciept, Orders
from celery import shared_task
from rest_framework.response import Response
from rest_framework import status


@shared_task
def add_meats_task(order_time,table_id,meats):
    serializer = Orders(order_time=order_time,table_id=table_id)
    serializer.save()
    for item in meats:
        meat = Meat.objects.get(pk=item['id'])
        serializer_reciept = OrderReciept(meat=meat,order_id=serializer.id,quantity=item['quantity'])
        meat.quantity = meat.quantity - item['quantity']
        if(meat.quantity < 0):
            serializer.delete()
            # return Response(f'{ meat.name } not enough',status=status.HTTP_400_BAD_REQUEST)
            return False
        serializer_reciept.save()
        meat.save()
    return True
    # return Response('', status=status.HTTP_201_CREATED)

@shared_task
def create_random_user_accounts(total):

    for i in range(total):
        username = 'TO{}'.format(get_random_string(10, string.ascii_letters))
        table = TablestableInStore(name=username)
        table.save()
    return '{} random users created with success!'.format(total)


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)