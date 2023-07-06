from django.db import models


class OrdemDeServico(models.Model):
    nome = models.CharField(max_length=512, blank=True, null=True)
    arquivo = models.FileField(
        upload_to="ordens_de_servico/", blank=True, null=True)
    valor = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Ordem de serviço"
        verbose_name_plural = "Ordens de serviço"


class Status(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Status"


class Resultado(models.Model):
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    erro = models.TextField(blank=True, null=True)
    incerteza = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{}: {}".format(self.status.nome, self.erro)


class Laboratorio(models.Model):
    nome = models.CharField(max_length=512)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Laboratório"


class Certificado(models.Model):
    numero = models.CharField(max_length=512, verbose_name="Número")
    arquivo = models.FileField(
        upload_to="certificados/", null=True, blank=True)

    def __str__(self):
        return self.numero


class Referencia(models.Model):
    nome = models.CharField(max_length=512)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Referência"


class Criterio(models.Model):
    nome = models.CharField(max_length=512)
    referencia = models.ForeignKey(
        Referencia, on_delete=models.CASCADE, verbose_name="Referência")

    def __str__(self):
        return "{}: {}".format(self.referencia.nome, self.nome)

    class Meta:
        verbose_name = "Critério"


class Calibracao(models.Model):
    certificado = models.ForeignKey(
        Certificado, on_delete=models.SET_NULL, null=True)
    criterio = models.ForeignKey(
        Criterio, on_delete=models.SET_NULL, null=True, verbose_name="Critério")
    resultado = models.ForeignKey(
        Resultado, on_delete=models.SET_NULL, null=True)
    instrumento = models.ForeignKey(
        "instrumentos.Instrumento", on_delete=models.CASCADE, related_name="calibracoes")
    laboratorio = models.ForeignKey(
        Laboratorio, on_delete=models.SET_NULL, null=True, verbose_name="Laboratório")
    ordem_de_servico = models.ForeignKey(
        OrdemDeServico, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Ordem de serviço")
    data = models.CharField(max_length=10, null=True, blank=True)
    data_proxima_calibracao = models.CharField(max_length=10, null=True, blank=True)
    data_proxima_checagem = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return "Calibração {} - {}".format(self.pk, self.instrumento.tag)

    class Meta:
        verbose_name = "Calibração"
        verbose_name_plural = "Calibrações"
        ordering = ("id",)
