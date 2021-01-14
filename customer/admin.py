from django.contrib import admin
from customer.models import TablestableInStore , Tabledailydate , Meat , Orders, TypeOfMeat
# Register your models here.
admin.site.register(TablestableInStore)
admin.site.register(Tabledailydate)
admin.site.register(Meat)
admin.site.register(Orders)
admin.site.register(TypeOfMeat)