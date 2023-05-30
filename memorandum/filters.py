import django_filters
from .models import Menorandum

class MemoFilter(django_filters.FilterSet):
    class Meta:
        model=Menorandum
        fields = ['nombre']
        exclude = ['email','slug','user','created_at','date_expiring','texto','archivos']
        