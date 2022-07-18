from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(trains)
admin.site.register(days)
admin.site.register(passenger)
admin.site.register(city)
admin.site.register(booking)