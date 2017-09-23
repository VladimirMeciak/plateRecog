from django.contrib import admin

# Register your models here.

from .models import Visitor, Plate

admin.site.register(Visitor)
admin.site.register(Plate)
