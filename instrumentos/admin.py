from django.contrib import admin
from import_export.fields import Field
from import_export.admin import ImportMixin
from import_export.widgets import IntegerWidget, CharWidget
from import_export.resources import ModelResource
from import_export.forms import ImportForm, ConfirmImportForm
from .models import Fabricante, Instrumento, Localizacao, Modelo, OrdemDeCompra, Status, TipoDeInstrumento
from calibracoes.models import Laboratorio, Certificado, OrdemDeServico, Criterio, Referencia, Status as StatusResultado, Resultado, Calibracao
from clientes.models import Cliente
from django.forms import ModelChoiceField

@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


@admin.register(Localizacao)
class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'fabricante')


@admin.register(OrdemDeCompra)
class OrdemDeCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'data')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


@admin.register(TipoDeInstrumento)
class TipoDeInstrumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_de_serie')

class InstrumentosImportForm(ImportForm):
   cliente = ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=True)

class InstrumentosConfirmImportForm(ConfirmImportForm):
    cliente = ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=True)


class InstrumentoResource(ModelResource):
    tag = Field(
        column_name = "Identificação (Tag)",
        attribute = "tag",
        widget = CharWidget()
    )
    descricao = Field(
        column_name = "Descrição",
        attribute = "descricao",
        widget = CharWidget()
    )
    observacoes = Field(
        column_name = "Observações Adicionais",
        attribute = "observacoes",
        widget = CharWidget()
    )

    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.cliente = self.cliente

    def before_import_row(self, row, cliente, **kwargs):
        self.cliente = cliente
        row = {key.strip(): value if value not in ['-', ''] else None for key, value in row.items()}
        localizacao = row["Localização"]
        status = row["Status"]
        ordem_de_compra = row["Ordem de Compra (aquisição)"]
        data_de_compra = row["Data de Compra (aquisição)"]

        fabricante = row["Fabricante"]
        modelo = row["Modelo"]
        numero_de_serie = row["Nº Série"]
        resolucao = row["Resolução"]
        unidade = row["Unidade"]
        faixa_nominal = row["Faixa nominal"]

        self.localizacao, created = Localizacao.objects.get_or_create(nome=localizacao)
        self.status, created = Status.objects.get_or_create(nome=status)
        self.ordem_de_compra = None
        if ordem_de_compra:
            self.ordem_de_compra, created = OrdemDeCompra.objects.get_or_create(nome=ordem_de_compra, data=data_de_compra)

        fabricante, created = Fabricante.objects.get_or_create(nome=fabricante)
        modelo, created = Modelo.objects.get_or_create(nome=modelo, fabricante=fabricante)
        self.tipo, created = TipoDeInstrumento.objects.get_or_create(modelo=modelo, unidade=unidade, faixa_nominal=faixa_nominal)

        if numero_de_serie:
            self.tipo.numero_de_serie = numero_de_serie
        if resolucao:
            self.tipo.resolucao = resolucao
        self.tipo.save()


    def after_import_row(self, row, row_result, **kwargs):
        row = {key.strip(): value if value not in ['-', ''] else None for key, value in row.items()}
        laboratorio = row["Laboratório de referência"]
        numero_certificado = row["Nº Certificado de calibração"]
        ordem_de_servico = row["Ordem de Serviço (calibração)"]
        valor_servico = row["Valor Serviço (calibração)"]
        referencia = row["Referencia do critério de aceitação"]
        criterio = row["Criterio de Aceitação"]
        resultado = row["Resultado"]
        erro = row["Erro"]
        data_calibracao = row["Data da Calibração"]
        data_proxima_calibracao = row["Data da Proxima Calibração"]
        data_proxima_checagem = row["Data da Proxima Checagem"]

        if ordem_de_servico:
            ordem_de_servico, created = OrdemDeServico.objects.get_or_create(nome=ordem_de_servico, valor=valor_servico)
        laboratorio, created = Laboratorio.objects.get_or_create(nome=laboratorio)
        status_resultado, created = StatusResultado.objects.get_or_create(nome=resultado)
        resultado, created = Resultado.objects.get_or_create(status=status_resultado, erro=erro)
        certificado, created = Certificado.objects.get_or_create(numero=numero_certificado)
        referencia, created = Referencia.objects.get_or_create(nome=referencia)
        criterio, created = Criterio.objects.get_or_create(nome=criterio, referencia=referencia)
        instrumento = Instrumento.objects.get(pk=row_result.object_id)
        instrumento.localizacao = self.localizacao
        instrumento.status = self.status
        if self.ordem_de_compra:
            instrumento.ordem_de_compra = self.ordem_de_compra
        instrumento.tipo = self.tipo
        instrumento.save()
        calibracao, created = Calibracao.objects.get_or_create(instrumento=instrumento, certificado=certificado, criterio=criterio, resultado=resultado, laboratorio=laboratorio, ordem_de_servico=ordem_de_servico, data=data_calibracao, data_proxima_calibracao=data_proxima_calibracao, data_proxima_checagem=data_proxima_checagem)


    class Meta:
        model = Instrumento
        import_id_fields = ('tag',)
        fields = ('tag', 'descricao', 'observacoes')
        export_order = ('tag', 'descricao', 'observacoes')


@admin.register(Instrumento)
class InstrumentoAdmin(ImportMixin, admin.ModelAdmin):
    resource_classes = [InstrumentoResource]
    import_form_class = InstrumentosImportForm
    confirm_form_class = InstrumentosConfirmImportForm

    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)
        if import_form:
            initial['cliente'] = import_form.cleaned_data['cliente']
        return initial

    def get_import_data_kwargs(self, request, *args, **kwargs):
        form = kwargs.get('form')
        if form:
            return form.cleaned_data
        return {}

    list_display = ('id', 'tag', 'tipo', 'cliente')
