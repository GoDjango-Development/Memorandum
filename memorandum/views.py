from django.shortcuts import render,redirect
from .models import Menorandum,Archivos,Invitacion,Destinatarios,Invitacion
from home.models import Empresa
from django.urls import reverse_lazy
from django.core.mail import send_mail,send_mass_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.html import strip_tags
from .forms import CrearMemorandumForm,ModificarMemorandumForm,ArchivosForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import UpdateView,DeleteView,DetailView
from datetime import date 
from .filters import MemoFilter

User=get_user_model()

# Create your views here.
@login_required
def memorandus(request):
    if request.user.is_authenticated:  
        empresa = Empresa.objects.first()
        memo = Menorandum.objects.filter(user=request.user).order_by('-created_at')
        filter=MemoFilter(request.GET,queryset=memo)
        memo=filter.qs       
        paginator = Paginator(memo, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'memo/list-memorandus.html',{'page_obj':page_obj,'filter':filter,'empresa':empresa})
        
    else:
        return redirect('loginn')
    
@login_required   
def add_memorandus(request):
    if request.method=='GET' and request.user.is_authenticated:
            empresa = Empresa.objects.first()
            return render(request, 'memo/add-memorandum.html', {'form': CrearMemorandumForm(),'empresa':empresa})
    
    
    if request.method=='POST' and request.user.is_authenticated :
        form = ArchivosForm(request.POST, request.FILES)
        if form.is_valid():
            
            """post=form.save(commit=False) 
            files=request.FILES.getlist('archivos')
            for f in files: 
                post.archivos=f
            post.email=request.user.email
            post.user=request.user
            post.save()"""
            
            m=Menorandum.objects.create(
                nombre=request.POST['nombre'],
                texto=request.POST['texto'],
                email=request.user.email,
                #date_expiring=request.POST['date_expiring'],
                user=request.user,       
            )
            if request.POST['date_expiring'] != '':
                m.date_expiring=request.POST['date_expiring'] 
            if request.FILES.getlist('archivos') != '':    
                for f in request.FILES.getlist('archivos'):
                    file_instance=Archivos(user=request.user,archivos=f,memo=m.nombre)
                    file_instance.save()
                    m.archivos.add(file_instance)           
            m.save()
            return redirect('list_memorandums')
        else:
            empresa = Empresa.objects.first()
            return render(request, 'memo/add-memorandum.html', {
            'error': 'El formulario no es valido','empresa':empresa
            })

def add_arch_memo(request,pk):
    if request.method=='GET' and request.user.is_authenticated:
            empresa = Empresa.objects.first()
            return render(request, 'memo/archivos/update-archivos.html', {'form': ArchivosForm(),'empresa':empresa})
        
    if request.method=='POST' and request.user.is_authenticated :  
        form = ArchivosForm(request.POST, request.FILES)
        if form.is_valid():      
            m=Menorandum.objects.filter(id=pk).first()
            if request.FILES.getlist('archivos') != '':    
                for f in request.FILES.getlist('archivos'):
                    file_instance=Archivos(user=request.user,archivos=f,memo=m.nombre)
                    file_instance.save()
                    m.archivos.add(file_instance) 
        return redirect('list_memorandums')
        
        
    
                
            
def memo_arch(request,nombre):
    ma=Archivos.objects.filter(memo=nombre)
    return render(request,"memo/archivos/list-archivos.html",{'archivos':ma})
    
def invitar_lector(request,nombre):
    if request.method=='GET' and request.user.is_authenticated:
        empresa=Empresa.objects.first()
        user=User.objects.exclude(is_superuser=True).exclude(username=request.user.username).values('email')
        
        dest=Destinatarios.objects.filter(nombre_memo=nombre).values('destinatario').distinct()
        destid=Destinatarios.objects.filter(destinatario__in=dest).filter(nombre_memo=nombre)
        print(destid)
        return render(request, 'emails/envio_emails.html', {'usuarios':user,'nombre':nombre,'empresa':empresa,'ids':destid})
    else:
        return redirect('list_memorandums')

                    
def invitar(request):  
    if request.method=='POST' and request.user.is_authenticated :
        
        n=request.POST['nombre']
        id=Menorandum.objects.filter(user=request.user.id,nombre=n).values('id').first()
        s=Menorandum.objects.filter(user=request.user.id,id=id["id"]).values('slug')  
        i=Invitacion.objects.create(
           nombre_memo=n,
           slug=s[0]['slug'],
           remitente=request.user.username,            
        )  
        for d in request.POST.getlist('email'):
                u=User.objects.filter(email=d).first()
                dest_instance=Destinatarios(destinatario=u,nombre_memo=n)
                dest_instance.save()
                i.destinatarios.add(dest_instance)  
        enviar_mail(               
                nombre=request.POST['nombre'],
                para=request.POST.getlist('email'),
                email=request.user.email,
                slug=s[0]['slug'],
            )
        i.save()
        return redirect('list_memorandums')
    else:
        return redirect('home')
        
def enviar_mail(**kwargs):
    asunto="Haz sido invitado a leer el siguiente Memorandumn"
    mensaje=render_to_string("emails/email.html",{
        "nombre":kwargs.get("nombre"),
        "email":kwargs.get("email"),
        "slug":kwargs.get("slug"),        
    })
    mensaje_texto=strip_tags(mensaje)
    from_email=settings.EMAIL_HOST_USER
    
    to=kwargs.get("para")
    for x in to:
        send_mail(asunto,mensaje_texto,from_email,[x],html_message=mensaje)        


def invitaciones(request):
    if request.user.is_authenticated:
        empresa=Empresa.objects.first()
        inv=Invitacion.objects.filter(destinatarios__in=Destinatarios.objects.filter(destinatario=request.user))
        return render(request,'memo/invitaciones/list-invitaciones.html',{'invitacion':inv,'empresa':empresa})
    
        
class UpdateMemo(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Menorandum
    form_class = ModificarMemorandumForm
    template_name = "memo/update_memo.html"
    success_url = reverse_lazy('list_memorandums')
    context_object_name='menorandum' 
    permission_required = 'memorandum.change_menorandum'
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['empresa']=Empresa.objects.first()
        m=Menorandum.objects.filter(id=self.object.id).values('nombre')
        a=m[0]['nombre']
        context['archivos']=Archivos.objects.filter(memo=a)
        
        return context
   
    
class UpdateArchivo(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Archivos
    form_class = ArchivosForm
    template_name = "memo/archivos/update-archivos.html"
    success_url = reverse_lazy('list_memorandums')
    context_object_name='archivo' 
    permission_required = 'memorandum.change_archivos'
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['empresa']=Empresa.objects.first()
        
        return context 

       
class DeleteMemo(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Menorandum
    template_name = "memo/delete_memo.html"
    success_url = reverse_lazy('list_memorandums')
    permission_required = 'memorandum.delete_menorandum'
    
class DeleteInvitado(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Destinatarios
    template_name = "memo/delete_memo.html"
    success_url = reverse_lazy('list_memorandums')
    permission_required = 'memorandum.delete_destinatarios'
    
class DeleteArchivo(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Archivos
    template_name = "memo/archivos/delete_archivo.html"
    success_url = reverse_lazy('list_memorandums')
    permission_required = 'memorandum.delete_archivos'
    
class DetailMemo(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    model = Menorandum
    context_object_name='menorandum'
    template_name = "memo/menorandum_detail.html"
    permission_required = 'memorandum.view_menorandum'
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['empresa']=Empresa.objects.first()
        m=Menorandum.objects.filter(id=self.object.id).values('date_expiring')
        desti=Destinatarios.objects.filter(nombre_memo=self.object.nombre).values('destinatario').distinct()
        al=Destinatarios.objects.filter(destinatario__in=desti) 
        a=m[0]['date_expiring']        
        #print(desti)        
        print(a)
        for x in al:
            if self.request.user.username == x.destinatario.username:
                context['invitado']=True
                 
        if a == None :
            context['expiro']=False
        else:
            if a <= date.today():
               context['expiro']=True 
         
        return context
    
    
        
            
    
    
