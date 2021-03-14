from django.db import models
from rest_framework import serializers
from django.core.serializers import serialize

from customer.models import OrderReciept, TablestableInStore , Tabledailydate , Meat , Orders, TypeOfMeat

class TableStableSerializers(serializers.ModelSerializer):
    class Meta :
        model = TablestableInStore
        fields = '__all__'

class TableDailySerializers(serializers.ModelSerializer):
    class Meta :
        model = Tabledailydate
        fields = '__all__'

class MeatSerializers(serializers.ModelSerializer):
    # meat_list = OrderSerializers(many=True)
    class Meta:
        model = Meat
        fields = '__all__'

class OrderSerializers(serializers.ModelSerializer):
    meats = MeatSerializers(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = '__all__'
        depth = 1

class OrderRecieptSerailizers(serializers.ModelSerializer):
    name = serializers.CharField(source='meat.name')
    class Meta: 
        model = OrderReciept
        fields = ('quantity','name')
        depth =1


class OrderWithThrouthSerializers(serializers.ModelSerializer):
    meat = OrderRecieptSerailizers(source='meat_to_order', many=True,read_only=True)
    class Meta:
        model = Orders
        fields = ('id', 'meat', 'status')
        depth = 1

class OrderManySerializers(serializers.ModelSerializer):
    meats = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Orders
        fields= '__all__'
        depth=1


class TypeOfMeatSerializers(serializers.ModelSerializer):
    class Meta:
        model = TypeOfMeat
        fields = '__all__'
        