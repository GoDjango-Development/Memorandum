from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.views.generic import RedirectView,View
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Empresa
from django.contrib.auth import get_user_model
from .forms import CambiarPasswordForm
from django.urls import reverse_lazy
User=get_user_model()


# Create your views here.


def loguear(request):
    if request.user.is_authenticated:
        
        return redirect('Home')
              
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            usu=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usuario=authenticate(username=usu, password=pwd)
            if usuario is not None:
                login(request, usuario)
                return redirect('Home')
            else:
                                
                return render(request,"registration/login.html",{"messages":"El Usuario o la Contraseña no son validos"})
        else:
                        
            return render(request,"registration/login.html",{"messages":"El Usuario o la Contraseña no son validos"})
                
    form=AuthenticationForm()        
    return render(request,"registration/login.html",{"form":form})
    
class Login(LoginView):
    template_name="registration/login.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
                return redirect('Home')
        return super().dispatch(request, *args, **kwargs)

class Salir(RedirectView):
    template_name="registration/logged_out.html"
    pattern_name='login'
    
@login_required
def home(request):
    empresa = Empresa.objects.first() 
    Memorandum=Group.objects.filter(name="Memorandum").first()
    print(Memorandum)
    request.user.groups.add(Memorandum)   
    return render(request, "memorandum/base.html",{'empresa':empresa})
@login_required
def contacto(request):
    empresa = Empresa.objects.first()
    return render(request, "memorandum/contact.html",{'empresa':empresa})

class CambiarPassword(LoginRequiredMixin,View):
    template_name='memorandum/cambiarpwd.html'
    form_class=CambiarPasswordForm
    success_url=reverse_lazy('Home')
    
    def get(self, request,*args,**kwargs):
        empresa = Empresa.objects.first()
        return render(request, self.template_name,{'form':self.form_class,'empresa':empresa})
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)  
        if form.is_valid():
            user=User.objects.filter(id=request.user.id)
            if user.exists():
                user=user.first()
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                return redirect(self.success_url)
            return redirect(self.success_url)
        else:
            empresa = Empresa.objects.first()
            error="El formulario no es válido"
            return render(request,self.template_name,{'error':error,'empresa':empresa})