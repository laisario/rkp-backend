from django.db import models
from django.contrib.auth.models import User


class Empresa(models.Model):
    razao_social = models.CharField(
        max_length=512, verbose_name="Razão Social")
    cnpj = models.CharField(max_length=25, verbose_name="C.N.P.J.")
    ie = models.CharField(max_length=50, verbose_name="Inscrição Estadual", null=True, blank=True)
    isento = models.BooleanField(default=False)

    def __str__(self):
        return self.razao_social


class Unidade(models.Model):
    nome = models.CharField(max_length=212)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name="unidades")

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(blank=True, null=True, max_length=112)
    empresa = models.OneToOneField(
        Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    telefone = models.CharField(max_length=25, null=True, blank=True)
    cpf = models.CharField(max_length=25, null=True,
                           blank=True, verbose_name="C.P.F.")
    endereco = models.ForeignKey(
        "enderecos.Endereco", on_delete=models.SET_NULL, null=True, verbose_name="Endereço")
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuário")

    def __str__(self):
        if hasattr(self.empresa, 'razao_social'):
            return self.empresa.razao_social
        if self.nome:
            return self.nome
        return super().__str__()
