from django.contrib import admin
from profiles.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city')
admin.site.register(Profile, ProfileAdmin)


