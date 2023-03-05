from django.contrib import admin
from .models import UserInfo, Clients, ClientImages, ClientComments
# Register your models here.



admin.site.register(UserInfo)
admin.site.register(Clients)
admin.site.register(ClientImages)
admin.site.register(ClientComments)