from django.db import models


class Status(models.Model):
    nome = models.CharField(max_length=512)
    cor = models.CharField(max_length=20, default="success")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Status"


class Instrumento(models.Model):
    tag = models.CharField(max_length=512)
    descricao = models.CharField(
        max_length=512, null=True, blank=True, verbose_name="Descrição"
    )
    modelo = models.CharField(max_length=512)
    fabricante = models.CharField(max_length=512)
    numero_de_serie = models.CharField(
        max_length=1024, null=True, blank=True, verbose_name="Número de série"
    )
    unidade = models.CharField(max_length=512)
    resolucao = models.DecimalField(
        default=0.0, max_digits=12, decimal_places=2, verbose_name="Resolução"
    )
    faixa_nominal_max = models.DecimalField(
        default=0.0,
        max_digits=12,
        decimal_places=2,
        verbose_name="Faixa nominal (máximo)",
    )
    faixa_nominal_min = models.DecimalField(
        default=0.0,
        max_digits=12,
        decimal_places=2,
        verbose_name="Faixa nominal (mínimo)",
    )
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(
        "clientes.Cliente", on_delete=models.CASCADE, related_name="instrumentos"
    )
    observacoes = models.TextField(null=True, blank=True, verbose_name="Observações")
    data_proxima_checagem = models.DateField(
        null=True, blank=True, verbose_name="Data da próxima checagem"
    )
    laboratorio = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return "{} - {}: {}".format(self.modelo, self.tag, self.cliente)


class Calibracao(models.Model):
    instrumento = models.ForeignKey(
        Instrumento,
        on_delete=models.CASCADE,
        related_name="calibracoes",
        verbose_name="Instrumento calibrado",
    )

    ordem_de_servico = models.CharField(
        max_length=512, blank=True, null=True, verbose_name="Ordem de serviço"
    )
    local = models.CharField(
        max_length=512, null=True, verbose_name="Local da calibração"
    )
    numero_do_certificado = models.CharField(
        max_length=512, verbose_name="Número do certificado"
    )
    certificado = models.FileField(upload_to="certificados/", null=True, blank=True)

    data = models.DateField(verbose_name="Data da calibração")
    data_proxima_calibracao = models.DateField(
        null=True, blank=True, verbose_name="Data da próxima calibração"
    )

    # Resultado
    aprovado = models.BooleanField()
    maior_erro = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)
    incerteza = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)
    criterio_de_aceitacao = models.DecimalField(
        default=0.0,
        max_digits=12,
        decimal_places=2,
        verbose_name="Critério de aceitação",
    )
    referencia_do_criterio = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name="Referência do critério de aceitação",
    )
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    def __str__(self):
        return "Calibração {} - {}".format(self.pk, self.instrumento.tag)

    def save(self, *args, **kwargs) -> None:
        self.aprovado = (
            abs(self.maior_erro) + abs(self.incerteza) < self.criterio_de_aceitacao
        )
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Calibração"
        verbose_name_plural = "Calibrações"
