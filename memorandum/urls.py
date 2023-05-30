"""Memorand URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import memorandus,add_memorandus,UpdateMemo,DeleteMemo,DetailMemo,invitar_lector,invitar,DeleteArchivo,memo_arch,UpdateArchivo,DeleteInvitado,invitaciones
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
   path('mismemos',memorandus,name="list_memorandums"),
   path('misinvitaciones',invitaciones,name="list_invitaciones"),
   path('memorandum_archivos/<str:nombre>',memo_arch,name="list_memorandums_archivos"),
   path('add_memo',add_memorandus,name="add_memorandums"),
   path('update_memo/<int:pk>',UpdateMemo.as_view(),name="update_memorandums"),
   path('update_archivo/<int:pk>',UpdateArchivo.as_view(),name="update_archivo"),
   path('delete_memo/<int:pk>',DeleteMemo.as_view(),name="delete_memorandums"),
   path('delete_archivo/<int:pk>',DeleteArchivo.as_view(),name="delete_archivo"),
   path('delete_invitado/<int:pk>',DeleteInvitado.as_view(),name="delete_invitados"),
   path('detail_memo/<str:username>/<int:pk>',DetailMemo.as_view(),name="detail_memorandums"),
   path('invitar_lector/<str:nombre>',invitar_lector,name="invitar_lector"),
   path('invitar',invitar,name="invitar"),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


