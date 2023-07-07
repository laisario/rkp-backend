from decimal import Decimal, InvalidOperation

from django.contrib import admin
from django.forms import ModelChoiceField
from import_export.admin import ImportMixin
from import_export.fields import Field
from import_export.forms import ConfirmImportForm, ImportForm
from import_export.resources import ModelResource
from import_export.tmp_storages import MediaStorage
from import_export.widgets import CharWidget

from clientes.models import Cliente

from .models import Calibracao, Instrumento, Status


def extract_number(string):
    chunks = string.split(" ")
    for chunk in chunks:
        try:
            return Decimal(chunk)
        except InvalidOperation:
            continue


@admin.register(Calibracao)
class CalibracaoAdmin(admin.ModelAdmin):
    list_display = ("id", "instrumento", "aprovado")


class InstrumentoResource(ModelResource):
    tag = Field(column_name="Identificação (Tag)", attribute="tag", widget=CharWidget())
    descricao = Field(
        column_name="Descrição", attribute="descricao", widget=CharWidget()
    )
    observacoes = Field(
        column_name="Observações Adicionais",
        attribute="observacoes",
        widget=CharWidget(),
    )

    def before_save_instance(self, instance, *args, **kwargs):
        instance.cliente = self.cliente

    def before_import_row(self, row, cliente, *args, **kwargs):
        self.cliente = cliente
        row = {
            key.strip(): value if value not in ["-", ""] else None
            for key, value in row.items()
        }
        status = row["Status"]
        self.status, _ = Status.objects.get_or_create(nome=status)

    def after_import_row(self, row, row_result, *args, **kwargs):
        row = {
            key.strip(): value if value not in ["-", ""] else None
            for key, value in row.items()
        }
        laboratorio = row["Laboratório de referência"]
        local = row["Localização"]
        data_calibracao = row["Data da Calibração"]
        data_proxima_calibracao = row["Data da Proxima Calibração"]
        data_proxima_checagem = row["Data da Proxima Checagem"]
        numero_certificado = row["Nº Certificado de calibração"]
        ordem_de_servico = row["Ordem de Serviço (calibração)"]
        erro = row["Erro"]
        criterio = row["Criterio de Aceitação"]
        referencia = row["Referencia do critério de aceitação"]
        fabricante = row["Fabricante"]
        modelo = row["Modelo"]
        resolucao = row["Resolução"]
        unidade = row["Unidade"]
        faixa_nominal = row["Faixa nominal"]
        numero_de_serie = row["Nº Série"]

        Instrumento.objects.filter(pk=row_result.object_id).update(
            modelo=modelo,
            status=self.status,
            data_proxima_checagem=data_proxima_checagem,
            laboratorio=laboratorio,
            modelo=modelo,
            fabricante=fabricante,
            numero_de_serie=numero_de_serie,
            unidade=unidade,
            resolucao=resolucao,
            faixa_nominal_min=extract_number(faixa_nominal),
            faixa_nominal_max=extract_number(faixa_nominal),
        )

        Calibracao.objects.get_or_create(
            instrumento__pk=row_result.object_id,
            ordem_de_servico=ordem_de_servico,
            local=local,
            numero_do_certificado=numero_certificado,
            data=data_calibracao,
            data_proxima_calibracao=data_proxima_calibracao,
            maior_erro=extract_number(erro),
            criterio_de_aceitacao=extract_number(criterio),
            referencia_do_criterio=referencia,
        )

    class Meta:
        model = Instrumento
        import_id_fields = ("tag",)
        fields = ("tag", "descricao", "observacoes")


class InstrumentosImportForm(ImportForm):
    cliente = ModelChoiceField(queryset=Cliente.objects.all(), required=True)


class InstrumentosConfirmImportForm(ConfirmImportForm):
    cliente = ModelChoiceField(queryset=Cliente.objects.all(), required=True)


@admin.register(Instrumento)
class InstrumentoAdmin(ImportMixin, admin.ModelAdmin):
    resource_classes = [InstrumentoResource]
    import_form_class = InstrumentosImportForm
    confirm_form_class = InstrumentosConfirmImportForm
    tmp_storage_class = MediaStorage

    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)
        if import_form:
            initial["cliente"] = import_form.cleaned_data["cliente"]
        return initial

    def get_import_data_kwargs(self, *args, **kwargs):
        form = kwargs.get("form")
        if form:
            return form.cleaned_data
        return {}

    list_display = ("id", "tag", "modelo", "cliente")
