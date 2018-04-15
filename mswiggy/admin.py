from django.contrib import admin

from .models import Restaurant, Customer, Driver, UpdateLocation, Menu


admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(UpdateLocation)
admin.site.register(Menu)
