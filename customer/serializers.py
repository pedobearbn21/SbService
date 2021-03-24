from django.db import models
from rest_framework import serializers
from django.core.serializers import serialize

from customer.models import OrderReciept, TablestableInStore , Tabledailydate , Meat , Orders, TypeOfMeat


class TableDailySerializers(serializers.ModelSerializer):
    class Meta :
        model = Tabledailydate
        fields = '__all__'

class TableStableSerializers(serializers.ModelSerializer):
    # table_use_id =TableDailySerializers(source='table_of_dailytable', many=True,read_only=True)
    table_dialy  = serializers.SerializerMethodField('get_table')
    def get_table(self, obj):
        table = Tabledailydate.objects.filter(table_id = obj.id).values().order_by('-id').first()
        serializer_class = TableDailySerializers
        return table
    class Meta :
        model = TablestableInStore
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
    # meat_id = serializers.IntegerField(source='meat.id')
    class Meta: 
        model = OrderReciept
        fields = '__all__'


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
        