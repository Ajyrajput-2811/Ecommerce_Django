from django.contrib import admin
from .models import *

# Register your models here.
class customerAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Customer,customerAdmin)

class productAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Product,productAdmin)
admin.site.register(Cart)
admin.site.register(Cartitem)
admin.site.register(ShippingAddress)


