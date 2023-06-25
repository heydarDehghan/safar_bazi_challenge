from django.contrib import admin
from managment.models import Residence, Booking, ExtraCapacityDetail, StandardCapacityDetail
# Register your models here.

admin.site.register(Residence)
admin.site.register(Booking)
admin.site.register(ExtraCapacityDetail)
admin.site.register(StandardCapacityDetail)
