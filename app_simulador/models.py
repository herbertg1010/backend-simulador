from django.db import models

class Topico(models.Model):
    nome_topico = models.CharField(max_length=100)
    def __str__(self):
        return self.nome_topico


class Questao(models.Model):
    pergunta = models.TextField()
    alternativa_a = models.CharField(max_length=255)
    alternativa_b = models.CharField(max_length=255)
    alternativa_c = models.CharField(max_length=255)
    alternativa_d = models.CharField(max_length=255)
    alternativa_e = models.CharField(max_length=255)
    resposta_correta = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')])
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='media/', blank=True, null=True)
    def __str__(self):
        return self.pergunta



