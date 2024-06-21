from django.urls import path
from api_simulador import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('questoes/', views.QuestaoImagemListView.as_view(), name='questoes'),
    path('topico/<int:topico_id>/', views.QuestoesPorTopicoAPIView.as_view(), name='topico'),
    path('inserir/',views.NovaQuestaoAPIView.as_view(),name='inserir'),
    path('pesquisa/',views.PesquisarQuestoes.as_view(),name='pesquisa'),
    path('questao/<int:pk>/delete/', views.ExcluirQuestaoAPIView.as_view(), name='questao-excluir'),
    path('questao/<int:pk>/editar/', views.EditarQuestaoAPIView.as_view(), name='questao-editar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

