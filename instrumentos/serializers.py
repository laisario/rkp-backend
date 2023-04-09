from rest_framework import serializers
from .models import Instrumento, Fabricante, Localizacao, Modelo, OrdemDeCompra, Status, TipoDeInstrumento
from calibracoes.serializers import CalibracaoSerializer


class FabricanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricante
        fields = "__all__"


class LocalizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizacao
        fields = "__all__"


class ModeloSerializer(serializers.ModelSerializer):
    fabricante = FabricanteSerializer()

    class Meta:
        model = Modelo
        fields = "__all__"


class OrdemDeCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemDeCompra
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class TipoDeInstrumentoSerializer(serializers.ModelSerializer):
    modelo = ModeloSerializer()

    class Meta:
        model = TipoDeInstrumento
        fields = "__all__"


class InstrumentoSerializer(serializers.ModelSerializer):
    tipo = TipoDeInstrumentoSerializer()
    status = StatusSerializer()
    localizacao = LocalizacaoSerializer()
    calibracoes = CalibracaoSerializer(many=True)
    ordem_de_compra = OrdemDeCompraSerializer()

    class Meta:
        model = Instrumento
        exclude = ["cliente"]
