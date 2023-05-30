from django import forms
from django.forms import ModelForm,DateField
from .models import Menorandum,Archivos
from ckeditor.widgets import CKEditorWidget

class DateInput(forms.DateInput):
    input_type='date'
    
class ArchivosForm(ModelForm):
    
    class Meta:
        model=Archivos
        fields = ['archivos']
        exclude = ['created_at','user','memo']
        widgets = {
            'archivos': forms.ClearableFileInput(attrs={'multiple': True}),
        }
       
    
class CrearMemorandumForm(ModelForm):    
    class Meta:
        model=Menorandum
        fields = ['nombre','texto','archivos','date_expiring']
        exclude = ['email','slug','user','created_at']
        widgets = {
            'date_expiring': DateInput(attrs={'required':False},format='%Y-%m-%d'),
            'archivos': forms.ClearableFileInput(attrs={'multiple': True}),
            'texto': CKEditorWidget(),
        }
        
        
class ModificarMemorandumForm(ModelForm):
    class Meta:
        model=Menorandum
        fields = ['nombre','texto','date_expiring']
        exclude = ['email','archivos','slug','user','created_at']
        widgets = {
            'date_expiring': DateInput(attrs={'required':False},format='%Y-%m-%d'),
            'texto': CKEditorWidget(),            
        }
        

    