from django.contrib import admin
from home.models import Empresa
from solo.admin import SingletonModelAdmin
# Register your models here.
admin.site.register(Empresa, SingletonModelAdmin)

