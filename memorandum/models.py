from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from datetime import date 
from django.contrib.sites.models import Site


User=get_user_model()

def user_directory_path(instance, filename):
    return "user_{0}/{1}/{2}".format(instance.user.username, instance.memo, filename)

class Archivos(models.Model):
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    archivos=models.FileField(upload_to=user_directory_path, null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    memo=models.CharField(verbose_name='Nombre del Memorandum',max_length=200, null=True)   

class Destinatarios(models.Model):
    destinatario=models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_memo=models.CharField(verbose_name='Nombre del Memorandum',max_length=200, null=True)
    
    class Meta:
            verbose_name="Destinatario"
            verbose_name_plural="Destinatarios"
    
    def __str__(self):
            return self.destinatario.username
   

class Invitacion(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    nombre_memo=models.CharField(verbose_name='Nombre del Memorandum',max_length=200, null=True)
    slug=models.SlugField(max_length=255, null=True, blank=True)
    remitente=models.CharField(verbose_name='Remitente',max_length=200)    
    destinatarios=models.ManyToManyField('Destinatarios')
    
    class Meta:
        verbose_name="Invitacion"
        verbose_name_plural="Invitaciones"
    
    def __str__(self):
            return self.nombre_memo
    
   
    
class Menorandum(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre=models.CharField(verbose_name='Título',max_length=200,unique=True)
    texto=RichTextField()
    email=models.EmailField(verbose_name='Correo Electrónico',max_length=255)
    archivos=models.ManyToManyField('Archivos',blank=True)
    date_expiring=models.DateField(verbose_name='Fecha de Expiración', null=True,blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    slug=models.SlugField(max_length=255, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def save(self,*args, **kwargs):
        m=Menorandum.objects.filter(date_expiring__lte=date.today())
        for a in m:
            if a.date_expiring == None:
                a.date_expiring=None
            else:             
                a.delete() 
               
        return super(Menorandum, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name="Memorandum"
        verbose_name_plural="Memorandums"
        permissions=(('can_download_file','Puede descargar archivos asociados'),)

    REQUIRED_FIELDS=['nombre','texto','email']
    
    def __str__(self):
        return self.nombre
    
    

def slug_generator(sender,instance,**kwargs):
    
    if not instance.slug:        
        instance.slug = Site.objects.get_current().domain + '/memos/detail_memo/' + str(instance.user.username) + '/' + str(instance.id)

post_save.connect(slug_generator, sender = Menorandum)



    
    