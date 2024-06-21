from rest_framework import generics, status
from app_simulador.models import Questao
from .serializers import QuestaoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class QuestaoImagemListView(generics.ListAPIView):
    serializer_class = QuestaoSerializer
    def get_queryset(self):
        return Questao.objects.exclude(imagem__isnull=True)         


class QuestoesPorTopicoAPIView(generics.ListAPIView):
    serializer_class = QuestaoSerializer
    def get_queryset(self):
        topico_id = self.kwargs['topico_id']
        return Questao.objects.filter(topico_id=topico_id).exclude(imagem__isnull=True)


class NovaQuestaoAPIView(APIView):
    def post(self, request):
        serializer = QuestaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
class PesquisarQuestoes(generics.ListAPIView):
    serializer_class = QuestaoSerializer
    def get_queryset(self):
        termo_pesquisa = self.request.query_params.get('termo', '') 
        return Questao.objects.filter(pergunta__icontains=termo_pesquisa)
    
    
class ExcluirQuestaoAPIView(APIView):
    def delete(self, request, pk, format=None):
        try:
            questao = Questao.objects.get(pk=pk)
            questao.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Questao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class EditarQuestaoAPIView(APIView):
    def put(self, request, pk, format=None):
        try:
            questao = Questao.objects.get(pk=pk)
        except Questao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QuestaoSerializer(questao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


