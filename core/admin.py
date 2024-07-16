from django.contrib import admin
from .models import User, Farmer, Consumer, Farm, eggInventory,expenseInventory
# Register your models here.

admin.site.register(User)
admin.site.register(Farmer)
admin.site.register(Consumer)
admin.site.register(Farm)
admin.site.register(eggInventory)
admin.site.register(expenseInventory)