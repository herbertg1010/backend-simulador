from django.shortcuts import render, redirect
from .models import Questao,Topico
from .forms import CadastroQuestao
import random
from random import sample


def home(request):
    return render(request,'home.html')


def inserir(request):
    if request.method == 'POST':
        form = CadastroQuestao(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inserir')  
    else:
        form = CadastroQuestao( request.POST or None)
    return render(request, 'inserir-questoes.html', {'form': form})


def pesquisar(request):
    questoes = Questao.objects.all()

    if request.method == 'POST':
        topico_escolhido = request.POST.get('topico')
        texto_pesquisa = request.POST.get('texto_pesquisa')

        if topico_escolhido:
            topico = Topico.objects.get(nome_topico=topico_escolhido)
            questoes = questoes.filter(topico=topico)

        if texto_pesquisa:
            questoes = questoes.filter(pergunta__icontains=texto_pesquisa)

    return render(request, 'pesquisar.html', {'questoes': questoes})


def personalizado(request):
    if request.method == 'POST':
            topico_escolhido = request.POST.get('topico')  
            topico = Topico.objects.get(nome_topico=topico_escolhido)
            questoes = Questao.objects.filter(topico=topico)
            return render(request, 'simulado-personalizado.html', {'questoes': questoes})
    return render(request, 'home.html') 


def resultado_personalizado(request):
    if request.method == 'POST':
        respostas_usuario = {key: value for key, value in request.POST.items() if key.startswith('alternativa_')}
        pontuacao = 0
        questoes = [] 

        for key, value in respostas_usuario.items():
            questao_id = int(key.split('_')[1])  
            alternativa_usuario = value  

            questao = Questao.objects.get(pk=questao_id)

            if alternativa_usuario == questao.resposta_correta:
                pontuacao += 1

            questoes.append({
                'pergunta': questao.pergunta,
                'alternativa_a': questao.alternativa_a,
                'alternativa_b': questao.alternativa_b,
                'alternativa_c': questao.alternativa_c,
                'alternativa_d': questao.alternativa_d,
                'alternativa_e': questao.alternativa_e,
                'resposta_correta': questao.resposta_correta,
                'resposta_usuario': alternativa_usuario,
                'correto': alternativa_usuario == questao.resposta_correta,
                'imagem': questao.imagem,  
            })

        numero_total_questoes = len(questoes)
        numero_questoes_corretas = sum(questao['correto'] for questao in questoes)

        return render(request, 'resultado_personalizado.html', {
            'pontuacao': pontuacao,
            'questoes': questoes,
            'numero_questoes_corretas': numero_questoes_corretas,
            'numero_total_questoes': numero_total_questoes,
        })

    return redirect('home')     


def gerar_simulado(request):
    questoes_disponiveis = list(Questao.objects.all())
    random.shuffle(questoes_disponiveis)
    questoes_para_simulado = questoes_disponiveis[:10]
    return render(request, 'simulado.html', {'questoes_para_simulado': questoes_para_simulado})


def resultados(request):
    if request.method == 'POST':
        respostas = {}
        for key, value in request.POST.items():
            if key.startswith('questao_'):
                questao_numero = key.replace('questao_', '')
                respostas[questao_numero] = value

        pontuacao = 0
        respostas_corretas = []
        questoes = Questao.objects.all()
        
        for questao in questoes:
            questao_numero = str(questao.pk)
            resposta_correta = questao.resposta_correta
            if questao_numero in respostas:
                resposta_usuario = respostas[questao_numero]
            else:
                resposta_usuario = None

            if resposta_usuario == resposta_correta:
                pontuacao += 1
            numero_de_questoes = Questao.objects.count()
            respostas_corretas.append({
                'questao': questao,
                'resposta_usuario': resposta_usuario,
                'resposta_correta': resposta_correta,
            })

        return render(request, 'resultado.html', {'pontuacao': pontuacao, 'respostas_corretas': respostas_corretas,'numero_de_questoes': numero_de_questoes})


def simulado_ranqueado(request):
    questoes_disponiveis = list(Questao.objects.all())
    
    if len(questoes_disponiveis) >= 10:
        questoes_para_simulado = sample(questoes_disponiveis, 10)
    else:
       
        questoes_para_simulado = questoes_disponiveis

    return render(request, 'simulado-ranqueado.html', {'questoes_para_simulado': questoes_para_simulado})

   
def resultado_ranqueado(request):
    if request.method == 'POST':
        respostas_usuario = {}
        pontuacao = 0
        respostas_corretas = {}
        questoes = Questao.objects.all()
        
        for questao in questoes:
            questao_id = str(questao.id)
            resposta_correta = questao.resposta_correta
            resposta_usuario = request.POST.get('questao_' + questao_id)
            
            if resposta_usuario == resposta_correta:
                pontuacao += 1

            respostas_usuario[questao_id] = resposta_usuario
            respostas_corretas[questao_id] = resposta_correta

        numero_de_questoes = Questao.objects.count()
        media = pontuacao / numero_de_questoes

        respostas_corretas_list = []
        for questao in questoes:
            questao_id = str(questao.id)
            respostas_corretas_list.append({
                'questao': questao,
                'resposta_usuario': respostas_usuario[questao_id],
                'resposta_correta': respostas_corretas[questao_id],
            })

        return render(request, 'resultado_ranqueado.html', {
            'pontuacao': pontuacao,
            'media': media,
            'respostas_corretas_list': respostas_corretas_list, 'numero_de_questoes': numero_de_questoes})
   
   
   

