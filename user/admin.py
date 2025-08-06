from django.contrib import admin
from .models import CustomUser


class CutomUserAdmin(admin.ModelAdmin):
    list_display = ('id','username','email')
admin.site.register(CustomUser, CutomUserAdmin)
