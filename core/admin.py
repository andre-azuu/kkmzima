from django.contrib import admin
from .models import User, Farmer, Consumer

# Register your models here.

admin.site.register(User)
admin.site.register(Farmer)
admin.site.register(Consumer)