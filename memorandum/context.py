from memorandum.models import Invitacion,Destinatarios

def cant_inv(request):
    if request.user.is_authenticated:
       inv=Invitacion.objects.filter(destinatarios__in=Destinatarios.objects.filter(destinatario=request.user)).count()
    else:
        inv="Debes hacer Login"   
    return {'c_invitacion':inv}