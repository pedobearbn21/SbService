from django.contrib import admin
from customer.models import TablestableInStore , Tabledailydate , Meat , Orders, TypeOfMeat, OrderReciept
# Register your models here.
admin.site.register(TablestableInStore)
admin.site.register(Tabledailydate)
admin.site.register(Meat)
admin.site.register(Orders)
admin.site.register(TypeOfMeat)
admin.site.register(OrderReciept)