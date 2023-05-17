from django.db import models


class Fabricante(models.Model):
    nome = models.CharField(max_length=512)

    def __str__(self):
        return self.nome


class Modelo(models.Model):
    nome = models.CharField(max_length=512)
    fabricante = models.ForeignKey(
        Fabricante, on_delete=models.CASCADE, related_name="modelos")

    def __str__(self):
        return "{} - {}".format(self.fabricante.nome, self.nome)


class TipoDeInstrumento(models.Model):
    modelo = models.ForeignKey(Modelo, on_delete=models.SET_NULL, null=True)
    numero_de_serie = models.CharField(
        max_length=1024, null=True, blank=True, verbose_name="Número de série")
    resolucao = models.CharField(
        max_length=512, null=True, blank=True, verbose_name="Resolução")
    unidade = models.CharField(max_length=512)
    faixa_nominal = models.CharField(max_length=512)

    def __str__(self):
        return "{} - {}: {}".format(self.modelo.fabricante.nome, self.modelo.nome, self.faixa_nominal)

    class Meta:
        verbose_name_plural = "Tipos de instrumento"


class Status(models.Model):
    nome = models.CharField(max_length=512)
    cor = models.CharField(max_length=20, default="success")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Status"


class Localizacao(models.Model):
    nome = models.CharField(max_length=512)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Localização"
        verbose_name_plural = "Localizações"


class OrdemDeCompra(models.Model):
    nome = models.CharField(max_length=512)
    arquivo = models.FileField(
        upload_to="ordens_de_compra/", null=True, blank=True)
    data = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Ordens de compra"


class Instrumento(models.Model):
    tipo = models.ForeignKey(
        TipoDeInstrumento, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    localizacao = models.ForeignKey(
        Localizacao, on_delete=models.SET_NULL, null=True, verbose_name="Localização")
    cliente = models.ForeignKey(
        "clientes.Cliente", on_delete=models.CASCADE, related_name="instrumentos")
    ordem_de_compra = models.ForeignKey(OrdemDeCompra, on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.CharField(max_length=512)
    descricao = models.TextField(
        null=True, blank=True, verbose_name="Descrição")
    observacoes = models.TextField(
        null=True, blank=True, verbose_name="Observações")

    def __str__(self):
        return "{} - {}: {}".format(self.tipo, self.tag, self.cliente)
