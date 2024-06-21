from rest_framework import serializers
from app_simulador.models import Questao, Topico

class QuestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questao
        fields = '__all__'
   
  
class TopicoSerializer(serializers.ModelSerializer):
    questoes = QuestaoSerializer(many=True, read_only=True)
    class Meta:
        model = Topico
        fields = '__all__'
        
        
 

