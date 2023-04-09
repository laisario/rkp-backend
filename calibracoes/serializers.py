from rest_framework import serializers
from .models import Calibracao, Certificado, Criterio, Laboratorio, OrdemDeServico, Referencia, Resultado, Status


class CertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = "__all__"


class LaboratorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratorio
        fields = "__all__"


class OrdemDeServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemDeServico
        fields = "__all__"


class ReferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referencia
        fields = "__all__"


class CriterioSerializer(serializers.ModelSerializer):
    referencia = ReferenciaSerializer()
    class Meta:
        model = Criterio
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class ResultadoSerializer(serializers.ModelSerializer):
    status = StatusSerializer()

    class Meta:
        model = Resultado
        fields = "__all__"


class CalibracaoSerializer(serializers.ModelSerializer):
    certificado = CertificadoSerializer()
    criterio = CriterioSerializer()
    resultado = ResultadoSerializer()
    laboratorio = LaboratorioSerializer()
    ordem_de_servico = OrdemDeServicoSerializer()

    class Meta:
        model = Calibracao
        fields = "__all__"