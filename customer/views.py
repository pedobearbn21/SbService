from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.views import View
from customer.models import TablestableInStore , Tabledailydate , Meat , Orders, OrderReciept
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from customer.serializers import OrderSerializers, MeatSerializers, TableDailySerializers, OrderManySerializers
from django.utils import timezone


# Create your views here.
@api_view(['POST'])
def orderoder(request):
    if request.method == 'POST' :
        serializer = Orders(order_time=request.data['order_time'],table_id=request.data['table_id'])
        serializer.save()
        for item in request.data['meats']:
            meat = Meat.objects.get(pk=item['id'])
            serializer_reciept = OrderReciept(meat=meat,order_id=serializer.id,quantity=item['quantity'])
            # serializer.meats.add(meat)
            meat.quantity = meat.quantity - item['quantity']
            if(meat.quantity < 0):
                serializer.delete()
                return Response(f'{ meat.name } not enough',status=status.HTTP_400_BAD_REQUEST)
            serializer_reciept.save()
            meat.save()
        return Response('', status=status.HTTP_201_CREATED)


class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializers
    queryset = Orders.objects.all()

class OrderIDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    lookup_field = 'id'
    serializer_class = OrderSerializers

class OrderPost(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializers

class MeatView(generics.ListCreateAPIView):
    queryset = Meat.objects.all()
    serializer_class = MeatSerializers

class MeatIDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meat.objects.all()
    lookup_field = 'id'
    serializer_class = MeatSerializers

class Search(generics.ListAPIView):
    serializer_class = MeatSerializers
    lookup_url_kwarg = 'type'

    def get_queryset(self):
        type_id = self.kwargs.get(self.lookup_url_kwarg)
        meatlist = Meats.objects.filter(type=type_id)
        return meatlist

class GraphTotalCustomer(generics.ListAPIView):
    serializer_class = TableDailySerializers
    
    def get_queryset(self):
        total = Tabledailydate.objects.filter(table_open_time__date = timezone.now())
        return total