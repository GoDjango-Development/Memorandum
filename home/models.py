from django.db import models
from solo.models import SingletonModel

class Empresa(SingletonModel):
    nombre = models.CharField(verbose_name='Nombre de la Empresa',max_length=50)
    logo = models.ImageField(verbose_name='Logo de la Empresa',upload_to="Empresa",null=True,blank=True)
    mision = models.TextField(verbose_name='Misión de la Empresa')
    vision = models.TextField(verbose_name='Visión de la Empresa')
    
    class Meta:
        verbose_name="Empresa"
        verbose_name_plural="Empresas"
        
    def __str__(self):
            return self.nombre

