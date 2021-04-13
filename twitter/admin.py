from django.contrib import admin

# Register your models here.
from django.contrib import admin

from twitter.models import TwitterHandle, TwitterMonthly

admin.site.register(TwitterHandle)
admin.site.register(TwitterMonthly)