from django.shortcuts import redirect, render
from django.urls import reverse
from noivos.models import Convidados, Presentes, Acompanhantes
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.

def convidados(request):
    token = request.GET.get('token')
    convidado = Convidados.objects.get(token=token)
    presentes = Presentes.objects.filter(reservado=False).order_by('-importancia')
    acompanhantes = Acompanhantes.objects.filter(acompanhante_de = convidado )
    return render(request, 'convidados.html', {'convidado': convidado, 'presentes': presentes, 'token': token, 'acompanhantes': acompanhantes})


def responder_presenca(request):
    resposta = request.GET.get('resposta')
    token = request.GET.get('token')
    convidado = Convidados.objects.get(token=token)
    if resposta not in ['C', 'R']:
        messages.add_message(request, constants.ERROR, 'Você deve confirmar ou recusar')
        return redirect(f'{reverse('convidados')}?token={token}')
    
    convidado.status = resposta
    convidado.save()

    return redirect(f'{reverse('convidados')}?token={token}')

def reservar_presente(request, id):
    token = request.GET.get('token')

    convidado = Convidados.objects.get(token=token)
    presente = Presentes.objects.get(id=id)

    presente.reservado=True
    presente.reservado_por = convidado
    presente.save()
    return redirect(f'{reverse('convidados')}?token={token}')


def listar_acompanhantes(request):
    token = request.GET.get('token')
    convidado = Convidados.objects.get(token=token)
    qtd_convidados = Acompanhantes.objects.filter(acompanhante_de = convidado ).count()
    print(qtd_convidados)

    if qtd_convidados == convidado.maximo_acompanhantes:
        messages.add_message(request, constants.ERROR, 'Você chegou no limite de convidados')
        return redirect(f'{reverse('convidados')}?token={token}')

    if request.method == 'POST':
        nome_acompanhante = request.POST.get('nome_acompanhante')
       
        acompanhante = Acompanhantes(
            nome_acompanhante=nome_acompanhante,
            acompanhante_de = convidado
        )

        acompanhante.save()

        return redirect(f'{reverse('convidados')}?token={token}')