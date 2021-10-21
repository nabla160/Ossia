from django.contrib import admin

from .models import Event

# Add event by admin page return a 502 error
admin.site.register(Event)
