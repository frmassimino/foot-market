from django.contrib import admin

# Register your models here.

from .models import Ipo, Bidder

admin.site.register(Ipo)
admin.site.register(Bidder)