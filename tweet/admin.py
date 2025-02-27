from django.contrib import admin
from .models import tweet
from .models import photo
from .models import premium_user
# Register your models here.
admin.site.register(tweet)
admin.site.register(photo)
admin.site.register(premium_user)

