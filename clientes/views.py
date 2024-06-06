from django.shortcuts import render
from django.http import HttpResponse, JsonResponse # protocolo em desenvolvimento web
from .models import Cliente, Ar
import re
from django.contrib import messages
from django.core import serializers
import json 
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404 #procura o id do cliente e caso ache retorna o objeto e se não achar retorna o erro 404


def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render (request, 'clientes.html',{'clientes':clientes_list})# retornando a requisição do usuario com o banco de dados
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        ares = request.POST.getlist('ar')
        marcas = request.POST.getlist('marca')
        anos = request.POST.getlist('ano')

        cliente = Cliente.objects.filter(cpf = cpf)
        if cliente.exists():
            messages.error(request,'O CPF inserido já está em uso.')
            return render(request, 'clientes.html',{'nome':nome,'sobrenome':sobrenome,'email':email, 'cpf':cpf, 'cpf_error': 'cpf' in request.POST, 'ares': zip(ares, marcas, anos)})
        
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
             messages.error(request, 'O e-mail inserido é inválido.' )
             return render(request, 'clientes.html',{'nome':nome,'sobrenome':sobrenome,'cpf':cpf, 'email':email, 'email_error': 'email' in request.POST, 'ares':zip(ares, marcas, anos)})
        
        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )

        cliente.save()

        for ar, marca, ano in zip(ares, marcas, anos): #iteração ordenada sem bagunças
            ar = Ar(ar = ar, marca=marca, ano = ano, cliente=cliente)
            ar.save()
        
        messages.success(request, 'Cliente cadastrado com sucesso.')
        return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}')

def att_cliente(request):
    id_cliente = request.POST.get('id_cliente') #atraves desse id eu busco os dados
    
    cliente = Cliente.objects.filter(id=id_cliente)
    ares = Ar.objects.filter(cliente=cliente[0])
    
    cliente_json = json.loads(serializers.serialize('json', cliente))[0] ['fields'] # eu acesso sempre a posição 0 pq eu sei que sempre vai ter um cliente
    cliente_id = json.loads(serializers.serialize('json', cliente))[0] ['pk']
    
    ares_json = json.loads(serializers.serialize('json', ares))
    ares_json = [{'fields': ar['fields'], 'id': ar['pk']} for ar in ares_json]
    data = {'cliente':cliente_json, 'ares': ares_json, 'cliente_id':cliente_id}
    return JsonResponse(data)



@csrf_exempt #estou falando que para o update_ar quando um usuario enviar um form sem o csrf ta tudo bem
def update_ar(request, id):
    nome_ar = request.POST.get('ar')
    marca = request.POST.get('marca')
    ano = request.POST.get('ano')
    ar = Ar.objects.get(id=id)

    ar.ar = nome_ar
    ar.marca = marca
    ar.ano = ano
    ar.save()
    return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}')

def excluir_ar(request, id):
    try:
        ar = Ar.objects.get(id=id)
        ar.delete()
        return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}')

    except:
        return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}') #reverse pega o nome da url e converte para uma url de fato

def update_cliente(request,id): 
    body = json.loads(request.body) #utilizo esse json loads para receber esses dados como um dicionario
    nome = body['nome']
    sobrenome = body['sobrenome']
    email = body['email']
    cpf = body['cpf']
    
    

    cliente = get_object_or_404(Cliente, id=id)
    try:
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf
        cliente.save()
        return JsonResponse({'status': '200', 'nome':nome, 'sobrenome':sobrenome, 'email':email, 'cpf':cpf}) #atraves dos status o meu front sabe como lidar com as situações
        
    except:
        return JsonResponse({'status':'500'})


