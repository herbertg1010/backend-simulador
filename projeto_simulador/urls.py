from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_simulador import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('inserir/', views.inserir,name='inserir'),
    path('pesquisar/',views.pesquisar,name='pesquisar'),
    path('personalizado/',views.personalizado,name='personalizado'),
    path('resultado_personalizado/',views.resultado_personalizado,name='resultado_personalizado'),
    path('simulado/',views.gerar_simulado,name='simulado'),
    path('resultados/',views.resultados,name='resultados'),
    path('ranqueado/',views.simulado_ranqueado,name='ranqueado'),
    path('resultado_ranqueado/',views.resultado_ranqueado,name='resultado_ranqueado'),  
    path('api/', include('api_simulador.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



