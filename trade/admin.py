from django.contrib import admin

# Register your models here.

from .models import Trade, Bid, Ask, SuccessTrade

admin.site.register(Trade)
admin.site.register(Bid)
admin.site.register(Ask)
admin.site.register(SuccessTrade)