import secrets
from django.urls import reverse
from django.db import models

# Create your models here.

class Convidados(models.Model):
    status_choices = (
        ('AC', 'Aguardando confirmação'),
        ('C', 'Confirmado'),
        ('R', 'Recusado')
    )

    nome_convidado = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=25, null=True, blank=True)
    maximo_acompanhantes = models.PositiveIntegerField(default=0)
    token = models.CharField(max_length=25)
    status = models.CharField(max_length=2, choices=status_choices, default='AC')

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(16)
        super(Convidados, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome_convidado


    @property
    def link_convite(self):
        return f'http://127.0.0.1:8000{reverse("convidados")}?token={self.token}'


class Presentes(models.Model):
    nome_presente = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='presentes')
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    importancia = models.PositiveIntegerField()
    reservado_por = models.ForeignKey(Convidados, null=True, blank=True, on_delete=models.DO_NOTHING)
    reservado = models.BooleanField(default=False)
    

    def __str__(self):
        return self.nome_presente
    

class Acompanhantes(models.Model):
    nome_acompanhante = models.CharField(max_length=100)
    acompanhante_de = models.ForeignKey(Convidados, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome_acompanhante



