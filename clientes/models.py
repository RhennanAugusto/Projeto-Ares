from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length = 50)#charfield são campos de texto e não ignora o 0 a esquerda.
    sobrenome = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50)
    cpf = models.CharField(max_length = 12)

    def __str__(self) -> str:
        return self.nome
    

class Ar(models.Model):
    ar = models.CharField(max_length = 50)
    marca = models.CharField(max_length = 50)
    ano = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    montagens = models.IntegerField(default = 0)
    consertos = models.IntegerField (default = 0)

 


    