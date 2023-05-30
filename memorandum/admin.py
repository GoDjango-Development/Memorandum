from django.contrib import admin
from .models import Menorandum,Invitacion,Destinatarios
#from solo.admin import SingletonModelAdmin
# Register your models here.

admin.site.register(Invitacion)
admin.site.register(Destinatarios)

class MenorandumAdmin(admin.ModelAdmin):
    list_filter=('nombre','created_at')
    search_fields=('nombre',)

admin.site.register(Menorandum,MenorandumAdmin)

