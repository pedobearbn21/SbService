from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.views import View
from customer.models import TablestableInStore , Tabledailydate , Meat , Orders, OrderReciept, TypeOfMeat
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from customer.serializers import MeatSerializers, OrderManySerializers, OrderRecieptSerailizers, OrderSerializers, OrderWithThrouthSerializers, TableDailySerializers, TableStableSerializers, TypeOfMeatSerializers
from django.utils import timezone
from customer.tasks import create_random_user_accounts, add_meats_task
from celery import group
from django.contrib import messages

@api_view(['GET'])
def taskGenUser(request,total):
    res = create_random_user_accounts.delay(total)
    res.get()
    messages.success(request, 'We are generating your random users! Wait a moment and refresh this page.')
    return HttpResponse('success')


# Create your views here.
@api_view(['POST'])
def orderoder(request):
    if request.method == 'POST' :
        order_time = request.data['order_time']
        table_id = request.data['table_id']
        meats = request.data['meats']
        # res = add_meats_task.delay(order_time,table_id,meats)
        serializer = Orders(order_time=request.data['order_time'],table_id=request.data['table_id'])
        serializer.save()
        for item in request.data['meats']:
            meat = Meat.objects.get(pk=item['id'])
            serializer_reciept = OrderReciept(meat=meat,order_id=serializer.id,quantity=item['quantity'])
            meat.quantity = meat.quantity - item['quantity']
            if(meat.quantity < 0):
                serializer.delete()
                return Response(f'{ meat.name } not enough',status=status.HTTP_400_BAD_REQUEST)
            serializer_reciept.save()
            meat.save()
        return Response('Success', status=status.HTTP_201_CREATED)
        # while not (res.ready()):
        #     pass
        # if (res.get()):
        #     return Response('', status=status.HTTP_201_CREATED)
        # else:
        #     return Response(f'Meat not enough',status=status.HTTP_400_BAD_REQUEST)


class TableStableView(generics.ListCreateAPIView):
    serializer_class = TableStableSerializers
    queryset = TablestableInStore.objects.all()

class TableStableIDView(generics.RetrieveUpdateAPIView):
    serializer_class = TableStableSerializers
    lookup_field = 'id'
    queryset = TablestableInStore.objects.all()

class TableView(generics.ListCreateAPIView):
    serializer_class = TableDailySerializers
    # queryset = Tabledailydate.objects.filter(status='OPEN')
    queryset = Tabledailydate.objects.filter(status='OPEN')

class TableViewUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TableDailySerializers
    lookup_field = 'id'
    queryset = Tabledailydate.objects.all()

class TableIDView(generics.ListAPIView):
    serializer_class = TableDailySerializers
    lookup_url_kwarg = 'table_id'

    def get_queryset(self):
        table_stable_id = self.kwargs.get(self.lookup_url_kwarg)
        table = Tabledailydate.objects.filter(table=table_stable_id,status='CLOSE')
        return table





class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderWithThrouthSerializers
    queryset = Orders.objects.all()

class OrderIDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    lookup_field = 'id'
    serializer_class = OrderWithThrouthSerializers

class OrderPost(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializers
    

class MeatView(generics.ListCreateAPIView):
    serializer_class = MeatSerializers
    queryset = Meat.objects.all()

class MeatIDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meat.objects.all()
    lookup_field = 'id'
    serializer_class = MeatSerializers


class TypesView(generics.ListCreateAPIView):
    queryset = TypeOfMeat.objects.all()
    serializer_class = TypeOfMeatSerializers



class Search(generics.ListAPIView):
    serializer_class = MeatSerializers
    lookup_url_kwarg = 'type'

    def get_queryset(self):
        type_id = self.kwargs.get(self.lookup_url_kwarg)
        meatlist = Meat.objects.filter(type=type_id)
        return meatlist

class SearchMeatByText(generics.ListAPIView):
    serializer_class = MeatSerializers
    lookup_url_kwarg = 'text'
    def get_queryset(self):
        return Meat.objects.filter(name__icontains = self.kwargs.get(self.lookup_url_kwarg))
    

class GraphTotalCustomer(generics.ListAPIView):
    serializer_class = TableDailySerializers
    
    def get_queryset(self):
        total = Tabledailydate.objects.filter(table_open_time__date = timezone.now())
        return total


# Order which alredy Order Meat and Search by table
class OrderSearhByTable(generics.ListAPIView):
    serializer_class = OrderWithThrouthSerializers
    lookup_url_kwarg = 'table_id'

    def get_queryset(self):
        table_search_id = self.kwargs.get(self.lookup_url_kwarg)
        order = Orders.objects.filter(table_id = table_search_id ).order_by('status','-id')
        return order


from django.db.models import Count, Sum
class OrRecReport(generics.ListAPIView):
    serializer_class = OrderWithThrouthSerializers
    def get_queryset(self):
        return Orders.objects.filter(order_time__date = timezone.now())

@api_view(['get'])
def MeatInNeed(request):
    serializer =  OrderReciept.objects.filter(order__status = 'ORDERED').values('meat').annotate(Sum('quantity'))
    for i in serializer:
        meat = Meat.objects.get(pk=i['meat'])
        i['meat'] = meat.name
    return Response(serializer, status=status.HTTP_200_OK)
# class MeatInNeed(generics.ListAPIView):
#     serializer_class = OrderRecieptSerailizers
#     def get_queryset(self):
#         return OrderReciept.objects.annotate(Sum('quantity')).values('meat')
    
    