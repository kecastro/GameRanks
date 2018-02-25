from django.contrib import admin

from .models import *

admin.site.register(Game)
admin.site.register(UserAccount)
admin.site.register(Exchange)
admin.site.register(TradeOption)